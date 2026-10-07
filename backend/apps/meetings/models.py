import uuid
import os

from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.utils import timezone
from datetime import datetime, time, timedelta

def nom_complet(user):
        return user.get_full_name() or user.get_username()

def fin_par_defaut(date, heure_debut):
    """Heure de fin supposée (début + 1 h) pour une réunion sans heure de fin."""
    fin = datetime.combine(date, heure_debut) + timedelta(hours=1)
    return fin.time() if fin.date() == date else time(23, 59)

def pv_upload_to(instance, filename):
    return f"pv/{instance.reunion_id}/{filename}"


class TypeReunion(models.TextChoices):
    TECHNIQUE = "TECHNIQUE", "Technique"
    PROJET = "PROJET", "Projet"
    FORMATION = "FORMATION", "Formation"
    DIRECTION = "DIRECTION", "Direction"
    URGENCE = "URGENCE", "Urgence"


class StatutReunion(models.TextChoices):
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

    def est_disponible(self, date, heure_debut, heure_fin=None, reunion_id=None):
        fin = heure_fin or fin_par_defaut(date, heure_debut)

        candidats = Reunion.objects.filter(
            lieu=self,
            date=date,
            statut__in=[
                StatutReunion.PLANIFIEE,
                StatutReunion.EN_COURS,
            ],
        )

        if reunion_id:
            candidats = candidats.exclude(pk=reunion_id)

        return not any(
            r.heure_debut < fin and r.fin_effective() > heure_debut
            for r in candidats
        )

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

    heure_fin = models.TimeField(
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=20,
        choices=TypeReunion.choices,
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutReunion.choices,
        default=StatutReunion.PLANIFIEE,
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

    def fin_effective(self):
        return self.heure_fin or fin_par_defaut(self.date, self.heure_debut)

    def terminer(self):
        self.statut = StatutReunion.TERMINEE
        self.save(update_fields=["statut"])

    def clean(self):
        errors = {}

        # 1) Nom déjà utilisé par une autre réunion
        if self.objet:
            doublon = Reunion.objects.filter(
                objet__iexact=self.objet.strip(),
                date=self.date
            ).exclude(pk=self.pk)
            if doublon.exists():
                errors["objet"] = "Une réunion avec ce nom existe déjà."

        # 2) Heures cohérentes (inchangé)
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            errors["heure_fin"] = "L'heure de fin doit être après l'heure de début."

        # 3) Lieu disponible (inchangé)
        elif self.lieu_id and self.date and self.heure_debut:
            if not self.lieu.est_disponible(
                self.date, self.heure_debut, self.heure_fin, self.pk
            ):
                errors[NON_FIELD_ERRORS] = "Ce lieu est déjà occupé pendant cette période."

        if errors:
            raise ValidationError(errors)

    @property
    def est_cloturee(self):
        return self.statut in (StatutReunion.TERMINEE, StatutReunion.ANNULEE)

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
    

class ProcesVerbal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reunion = models.OneToOneField(
        Reunion,
        on_delete=models.CASCADE,
        related_name="pv",
    )

    contenu = models.TextField("Détails de la réunion")
    resultats = models.TextField("Résultats / décisions", blank=True)

    document = models.FileField(
        "Document joint",
        upload_to=pv_upload_to,
        blank=True,
        validators=[FileExtensionValidator(
            ["pdf", "doc", "docx", "odt", "xls", "xlsx", "ppt", "pptx", "txt", "png", "jpg", "jpeg"]
        )],
    )

    redacteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pv_rediges",
    )
    redacteur_nom = models.CharField(max_length=255, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    @property
    def nom_document(self):
        return os.path.basename(self.document.name) if self.document else ""

    def save(self, *args, **kwargs):
        if self.redacteur_id and not self.redacteur_nom:
            self.redacteur_nom = nom_complet(self.redacteur)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PV – {self.reunion}"
