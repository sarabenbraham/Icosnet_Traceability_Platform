from django.db import models
from multiselectfield import MultiSelectField


class FicheApplicative(models.Model):

    class Domaine(models.TextChoices):
        RH = "RH", "RH"
        COMMERCIAL = "COMMERCIAL", "Commercial"
        TECHNIQUE = "TECHNIQUE", "Technique / Telco"
        MIDDLEWARE = "MIDDLEWARE", "Middleware"
        BI = "BI", "Décisionnel"

    class Criticite(models.TextChoices):
        CRITIQUE = "CRITIQUE", "Critique"
        MAJEURE = "MAJEURE", "Majeure"
        MINEURE = "MINEURE", "Mineure"

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", "Brouillon"
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        EN_VALIDATION = "EN_VALIDATION", "En validation"
        VALIDEE = "VALIDEE", "Validée"
        REFUSEE = "REFUSEE", "Refusée"

    nom_application = models.CharField(max_length=200)

    code_application = models.CharField(
        max_length=50,
        unique=True
    )

    domaine_fonctionnel = MultiSelectField(
        choices=Domaine.choices,
        max_length=100,
    )

    criticite = models.CharField(
        max_length=20,
        choices=Criticite.choices
    )

    description = models.TextField(blank=True)

    ingenieur = models.ForeignKey(
        "users.Ingenieur",
        on_delete=models.PROTECT,
        related_name="fiches"
    )

    departements = models.ManyToManyField(
        "organization.Departement",
        related_name="fiches",
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.BROUILLON
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Fiche applicative"
        verbose_name_plural = "Fiches applicatives"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.nom_application} ({self.code_application})"
