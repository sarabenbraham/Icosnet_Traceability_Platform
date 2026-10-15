from django.conf import settings
from django.db import models
from django.utils import timezone


class Compte(models.Model):

    class Statut(models.TextChoices):
        ACTIF = "ACTIF", "Actif"
        DESACTIVE = "DESACTIVE", "Désactivé"

    class TypeCompte(models.TextChoices):
        GENERIQUE = "generique", "Compte générique"
        MESSAGERIE = "messagerie", "Compte messagerie"

    type_compte = models.CharField(
        max_length=20,
        choices=TypeCompte.choices,
        default=TypeCompte.GENERIQUE,
        verbose_name="Type de compte",
    )

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="compte",
    )

    email_connexion = models.EmailField(unique=True)

    mot_de_passe = models.CharField(max_length=128)

    date_creation = models.DateTimeField(auto_now_add=True)

    date_expiration = models.DateField(
        null=True,
        blank=True,
    )

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.ACTIF,
    )

    expire = models.BooleanField(default=False)

    archive = models.BooleanField(default=False, verbose_name="Archivé")
    date_archivage = models.DateTimeField(null=True, blank=True, verbose_name="Date d'archivage")

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.mot_de_passe)

    def verifier_expiration(self):
        if (
            self.date_expiration
            and self.date_expiration < timezone.localdate()
            and self.statut == self.Statut.ACTIF
        ):
            self.expire = True
            self.save(update_fields=["expire"])
            return True

        return False

    def __str__(self):
        return f"{self.email_connexion} - {self.statut}"