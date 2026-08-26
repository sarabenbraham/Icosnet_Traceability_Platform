from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class Stockage(models.Model):

    class Emplacement(models.TextChoices):
        LOCAL_VM = "LOCAL_VM", "Local VM"
        NAS = "NAS", "NAS"
        OBJET = "OBJET", "Stockage Objet"
        GED = "GED", "GED Externe"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="stockage"
    )

    persistance = models.BooleanField(
        default=False
    )

    emplacements = models.JSONField(
        default=list
    )

    def clean(self):
        erreurs = {}

        if self.persistance and not self.emplacements:
            erreurs["emplacements"] = (
                "Au moins un emplacement est obligatoire."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Stockage - {self.fiche.nom_application}"
