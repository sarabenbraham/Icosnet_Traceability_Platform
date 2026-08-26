from django.db import models

from .ficheApplicative import FicheApplicative


class ModuleMetier(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="module_metier"
    )

    modules = models.JSONField(
        default=list
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Modules métier - {self.fiche.nom_application}"
