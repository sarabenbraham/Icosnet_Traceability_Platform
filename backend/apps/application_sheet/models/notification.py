from django.conf import settings
from django.db import models

from .ficheApplicative import FicheApplicative


class Notification(models.Model):

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_fiches"
    )

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.CharField(
        max_length=255
    )

    lue = models.BooleanField(
        default=False
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.destinataire} - {self.message}"


class HistoriqueValidation(models.Model):

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="historique"
    )

    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="validations_fiches"
    )

    ancien_statut = models.CharField(
        max_length=20
    )

    nouveau_statut = models.CharField(
        max_length=20
    )

    commentaire = models.TextField(
        blank=True
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.fiche} : {self.ancien_statut} -> {self.nouveau_statut}"