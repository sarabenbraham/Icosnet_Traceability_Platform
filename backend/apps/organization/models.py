from django.db import models


class Direction(models.Model):
    nom = models.CharField(max_length=100)

    directeur = models.OneToOneField(
        "users.Directeur",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direction"
    )

    def __str__(self):
        return self.nom


class Departement(models.Model):
    nom = models.CharField(max_length=100)

    direction = models.ForeignKey(
        Direction,
        on_delete=models.CASCADE,
        related_name="departements"
    )

    chef_departement = models.OneToOneField(
        "users.ChefDepartement",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departement"
    )

    def __str__(self):
        return self.nom