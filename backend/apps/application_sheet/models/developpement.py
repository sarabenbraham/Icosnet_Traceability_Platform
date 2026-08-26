from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class Developpement(models.Model):

    class ModeDeveloppement(models.TextChoices):
        INTERNE = "INTERNE", "Développé en interne"
        EXTERNE = "EXTERNE", "Éditeur externe"

    class Environnement(models.TextChoices):
        PRODUCTION = "PRODUCTION", "Production"
        PREPROD = "PREPROD", "Pré-production"
        DEVELOPPEMENT = "DEVELOPPEMENT", "Développement"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="developpement"
    )

    mode_developpement = models.CharField(
        max_length=20,
        choices=ModeDeveloppement.choices
    )

    gestion_sources = models.CharField(
        max_length=300,
        blank=True
    )

    processus_ci_cd = models.TextField(
        blank=True
    )

    environnements = models.JSONField(
        default=list
    )

    methode_personnalisation = models.TextField(
        blank=True
    )

    livrables_personnalisation = models.TextField(
        blank=True
    )

    services = models.TextField(
        blank=True
    )

    def clean(self):
        erreurs = {}

        if (
            self.mode_developpement == self.ModeDeveloppement.INTERNE
            and not self.gestion_sources
        ):
            erreurs["gestion_sources"] = (
                "Un dépôt Git est obligatoire "
                "pour un développement interne."
            )

        if not self.environnements:
            erreurs["environnements"] = (
                "Sélectionnez au moins un environnement."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Développement - {self.fiche.nom_application}"
