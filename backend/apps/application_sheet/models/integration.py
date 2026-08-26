from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class Integration(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="integration"
    )

    active_directory = models.BooleanField(
        default=False
    )

    groupes_ad = models.TextField(
        blank=True
    )

    messagerie = models.CharField(
        max_length=200,
        blank=True
    )

    compte_messagerie = models.CharField(
        max_length=200,
        blank=True
    )

    usage = models.CharField(
        max_length=200,
        blank=True
    )

    integration_bi = models.BooleanField(
        default=False
    )

    methode_bi = models.CharField(
        max_length=200,
        blank=True
    )

    def clean(self):
        erreurs = {}

        if self.active_directory and not self.groupes_ad:
            erreurs["groupes_ad"] = (
                "Les groupes Active Directory sont obligatoires."
            )

        if self.integration_bi and not self.methode_bi:
            erreurs["methode_bi"] = (
                "La méthode d'intégration BI est obligatoire."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Intégration - {self.fiche.nom_application}"
