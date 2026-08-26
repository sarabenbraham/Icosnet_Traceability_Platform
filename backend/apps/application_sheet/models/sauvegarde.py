from django.db import models

from .ficheApplicative import FicheApplicative


class Sauvegarde(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="sauvegarde"
    )

    emplacement_logs = models.TextField(
        blank=True
    )

    supervision = models.CharField(
        max_length=200,
        blank=True
    )

    sauvegarde_planifiee = models.BooleanField(
        default=False
    )

    outil = models.CharField(
        max_length=200,
        blank=True
    )

    recurrence = models.CharField(
        max_length=100,
        blank=True
    )

    heure = models.TimeField(
        null=True,
        blank=True
    )

    console_backup = models.URLField(
        blank=True
    )

    def __str__(self):
        return f"Sauvegarde - {self.fiche.nom_application}"
