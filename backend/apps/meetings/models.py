import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def nom_complet(user):
        return user.get_full_name() or user.get_username()

class TypeReunion(models.TextChoices):
    TECHNIQUE = "TECHNIQUE", "Technique"
    PROJET = "PROJET", "Projet"
    FORMATION = "FORMATION", "Formation"
    DIRECTION = "DIRECTION", "Direction"
    URGENCE = "URGENCE", "Urgence"


class StatutReunion(models.TextChoices):
    CREEE = "CREEE", "Créée"
    PLANIFIEE = "PLANIFIEE", "Planifiée"
    EN_COURS = "EN_COURS", "En cours"
    TERMINEE = "TERMINEE", "Terminée"
    ANNULEE = "ANNULEE", "Annulée"


class StatutParticipation(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", "En attente"
    CONFIRMEE = "CONFIRMEE", "Confirmée"
    REFUSEE = "REFUSEE", "Refusée"


class Lieu(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nom_salle = models.CharField(
        "Nom du lieu",
        max_length=150,
    )

    places_illimitees = models.BooleanField(
        "Places illimitées",
        default=False,
    )

    capacite = models.PositiveIntegerField(
        "Capacité",
        null=True,
        blank=True,
    )

    @property
    def capacite_label(self):
        if self.places_illimitees or self.capacite is None:
            return "Places illimitées"
        return f"{self.capacite} places"


    def __str__(self):
        return f"{self.nom_salle} ({self.capacite_label})"

    def clean(self):
        if self.places_illimitees:
            self.capacite = None
        elif not self.capacite:
            raise ValidationError(
                {"capacite": "Indiquez une capacité ou cochez « Places illimitées »."}
            )

    def est_disponible(self, date, heure_debut, heure_fin, reunion_id=None):
        conflits = Reunion.objects.filter(
            lieu=self,
            date=date,
            statut__in=[
                StatutReunion.CREEE,
                StatutReunion.PLANIFIEE,
                StatutReunion.EN_COURS,
            ],
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut,
        )

        if reunion_id:
            conflits = conflits.exclude(pk=reunion_id)

        return not conflits.exists()


class Reunion(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    objet = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    date = models.DateField()

    heure_debut = models.TimeField()

    heure_fin = models.TimeField()

    type = models.CharField(
        max_length=20,
        choices=TypeReunion.choices,
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutReunion.choices,
        default=StatutReunion.CREEE,
    )

    organisateur = models.CharField(
        max_length=255,
    )

    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="reunions",
        null=True,
        blank=True,
    )

    def clean(self):
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            raise ValidationError("L'heure de fin doit être après l'heure de début.")

        if self.lieu_id and self.date and self.heure_debut and self.heure_fin:
            if not self.lieu.est_disponible(
                self.date, self.heure_debut, self.heure_fin, self.pk
            ):
                raise ValidationError("Ce lieu est déjà occupé pendant cette période.")

    @property
    def nb_participants(self):
        return self.participations.exclude(
            statut=StatutParticipation.REFUSEE
        ).count()

    @property
    def est_complete(self):
        lieu = self.lieu
        return bool(
            lieu
            and not lieu.places_illimitees
            and lieu.capacite is not None
            and self.nb_participants >= lieu.capacite
        )

    def __str__(self):
        return f"{self.objet} - {self.date}"


class Participation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reunion = models.ForeignKey(
        Reunion,
        on_delete=models.CASCADE,
        related_name="participations",
    )

    # Utilisateur de la plateforme (vide pour un invité externe)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="participations_reunions",
    )

    # Nom affiché : copie du nom de l'utilisateur, ou nom/email de l'externe
    participant = models.CharField(max_length=255)

    date_confirmation = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=100, blank=True)

    statut = models.CharField(
        max_length=20,
        choices=StatutParticipation.choices,
        default=StatutParticipation.EN_ATTENTE,
    )

    class Meta:
        constraints = [
            # Un utilisateur ne peut être invité qu'une fois par réunion
            models.UniqueConstraint(
                fields=["reunion", "utilisateur"],
                condition=models.Q(utilisateur__isnull=False),
                name="unique_utilisateur_reunion",
            ),
            # Un externe (même nom) ne peut être ajouté qu'une fois par réunion
            models.UniqueConstraint(
                fields=["reunion", "participant"],
                condition=models.Q(utilisateur__isnull=True),
                name="unique_externe_reunion",
            ),
        ]

    @property
    def est_externe(self):
        return self.utilisateur_id is None

    def save(self, *args, **kwargs):
        if self.utilisateur_id and not self.participant:
            self.participant = nom_complet(self.utilisateur)
        super().save(*args, **kwargs)

    def confirmer(self):
        self.statut = StatutParticipation.CONFIRMEE
        self.date_confirmation = timezone.now()
        self.save(
            update_fields=[
                "statut",
                "date_confirmation",
            ]
        )

    def refuser(self):
        self.statut = StatutParticipation.REFUSEE
        self.date_confirmation = timezone.now()
        self.save(
            update_fields=[
                "statut",
                "date_confirmation",
            ]
        )

    def __str__(self):
        return f"{self.participant} - {self.reunion}"
    
    