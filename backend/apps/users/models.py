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
        help_text="Cocher si cet ingénieur peut traiter les tickets Help Desk."
    )
    est_directeur_systeme = models.BooleanField(
        default=False,
        verbose_name="Directeur Système",
        help_text="Cocher si cet ingénieur est Directeur Système et possède les privilèges de gestion des comptes."
    )

    def remplirFormulaire(self):
        pass

    def __str__(self):
        label = super().__str__()
        roles = []
        if self.est_helpdesk:
            roles.append("Help Desk")
        if self.est_directeur_systeme:
            roles.append("Directeur Système")
        if roles:
            label += f" [{', '.join(roles)}]"
        return label

class ChefDepartement(User):
    def valider(self):
        pass

    def refuser(self):
        pass

class Directeur(User):
    def valider(self):
        pass

    def refuser(self):
        pass

    def __str__(self):
        return super().__str__()
