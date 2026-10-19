from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class FluxApplication(models.Model):

    class TypeFlux(models.TextChoices):
        API = "API", "API REST"
        WEBHOOK = "WEBHOOK", "Webhook"
        AUTRE = "AUTRE", "Autre"

    class Sens(models.TextChoices):
        RECEPTION = "RECEPTION", "Réception"
        ENVOI = "ENVOI", "Envoi"

    # ForeignKey (et non plus OneToOne) : plusieurs flux par fiche
    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="flux"
    )

    solution_distante = models.CharField(
        max_length=200
    )

    adresse = models.CharField(
        max_length=255,
        blank=True
    )

    port = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    sens = models.CharField(
        max_length=10,
        choices=Sens.choices
    )

    type_flux = models.CharField(
        max_length=20,
        choices=TypeFlux.choices,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["id"]

    def clean(self):
        if self.port is not None and not (
            1 <= self.port <= 65535
        ):
            raise ValidationError({
                "port":
                "Le port doit être compris entre 1 et 65535."
            })

    def __str__(self):
        return f"Flux - {self.fiche.nom_application} - {self.solution_distante}"