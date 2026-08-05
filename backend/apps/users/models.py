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
    def remplirFormulaire(self):
        pass

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