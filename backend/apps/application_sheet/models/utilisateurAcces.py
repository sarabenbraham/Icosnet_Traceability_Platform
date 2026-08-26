from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class UtilisateurAcces(models.Model):

    class Canal(models.TextChoices):
        WEB = "WEB", "Navigateur Web"
        API = "API", "API"
        MOBILE = "MOBILE", "Application Mobile"
        CLI = "CLI", "Client Lourd"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="acces"
    )

    utilisateurs_cibles = models.TextField()

    profils_utilisateurs = models.TextField(
        blank=True
    )

    canaux_acces = models.JSONField(
        default=list
    )

    def clean(self):
        erreurs = {}

        if not self.utilisateurs_cibles:
            erreurs["utilisateurs_cibles"] = (
                "Les utilisateurs cibles sont obligatoires."
            )

        if not self.canaux_acces:
            erreurs["canaux_acces"] = (
                "Au moins un canal d'accès doit être sélectionné."
            )

        valides = {
            c[0] for c in self.Canal.choices
        }

        invalides = [
            valeur
            for valeur in self.canaux_acces
            if valeur not in valides
        ]

        if invalides:
            erreurs["canaux_acces"] = (
                f"Canaux invalides : {', '.join(invalides)}."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Accès - {self.fiche.nom_application}"
