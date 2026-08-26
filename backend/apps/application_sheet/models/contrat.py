from django.db import models

from .ficheApplicative import FicheApplicative


class Contrat(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="contrat"
    )

    fournisseur = models.CharField(
        max_length=200
    )

    budget_annuel = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    support_externe = models.BooleanField(
        default=False
    )

    reference_contrat = models.CharField(
        max_length=100,
        blank=True
    )

    date_debut = models.DateField(
        null=True,
        blank=True
    )

    date_fin = models.DateField(
        null=True,
        blank=True
    )

    prestataire = models.CharField(
        max_length=200,
        blank=True
    )

    pays = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"Contrat - {self.fiche.nom_application}"
