from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    poste = models.CharField(max_length=100, blank=True )

    def create(self):
        pass

    def modifier(self):
        pass

    def search(self):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Ingenieur(User):
    departement = models.ForeignKey(
        "organization.Departement",
        on_delete=models.CASCADE,
        related_name="ingenieurs",
        null=True,
        blank=True,
    )
    est_helpdesk = models.BooleanField(
        default=False,
        verbose_name="Agent Help Desk",
        help_text="Cocher si cet ing\u00e9nieur peut traiter les tickets Help Desk."
    )

    def remplirFormulaire(self):
        pass

    def __str__(self):
        label = super().__str__()
        if self.est_helpdesk:
            label += " [Help Desk]"
        return label

class ChefDepartement(User):
    def valider(self):
        pass

    def refuser(self):
        pass

class Directeur(User):
    est_directeur_systeme = models.BooleanField(
        default=False,
        verbose_name="Directeur Système",
        help_text="Cocher si ce directeur est Directeur Système et possède les privilèges de gestion des comptes."
    )

    def valider(self):
        pass

    def refuser(self):
        pass

    def __str__(self):
        label = super().__str__()
        if self.est_directeur_systeme:
            label += " [Directeur Système]"
        return label