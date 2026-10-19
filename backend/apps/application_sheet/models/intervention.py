from django.db import models

from .ficheApplicative import FicheApplicative


class Intervention(models.Model):

    class StatutIntervention(models.TextChoices):
        SUCCES = "SUCCES", "Succès"
        ECHEC = "ECHEC", "Échec"
        ROLLBACK = "ROLLBACK", "Rollback"

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="interventions"
    )

    date_heure = models.DateTimeField(
        null=True,
        blank=True
    )

    intervenant = models.CharField(
        max_length=200,
        blank=True
    )

    type_intervention = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutIntervention.choices,
        blank=True
    )

    class Meta:
        ordering = ["-date_heure"]

    def __str__(self):
        return f"Intervention - {self.fiche.nom_application}"
