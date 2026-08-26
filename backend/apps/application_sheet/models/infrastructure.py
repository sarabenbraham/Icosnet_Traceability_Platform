from django.core.exceptions import ValidationError
from django.db import models

from .ficheApplicative import FicheApplicative


class Infrastructure(models.Model):

    class TypeInfrastructure(models.TextChoices):
        ON_PREMISE = "ON_PREMISE", "On-Premise"
        CLOUD = "CLOUD", "Cloud"

    class TypeCloud(models.TextChoices):
        IAAS = "IAAS", "IaaS"
        PAAS = "PAAS", "PaaS"
        SAAS = "SAAS", "SaaS"

    class Virtualisation(models.TextChoices):
        PROXMOX = "PROXMOX", "Proxmox"
        VMWARE = "VMWARE", "VMware"
        DOCKER = "DOCKER", "Docker / Kubernetes"
        PHYSIQUE = "PHYSIQUE", "Serveur Physique"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="infrastructure"
    )

    type_infrastructure = models.CharField(
        max_length=20,
        choices=TypeInfrastructure.choices
    )

    type_cloud = models.CharField(
        max_length=10,
        choices=TypeCloud.choices,
        null=True,
        blank=True
    )

    plateforme_virtualisation = models.CharField(
        max_length=30,
        choices=Virtualisation.choices
    )

    cluster = models.CharField(
        max_length=200,
        blank=True
    )

    machine = models.CharField(
        max_length=200,
        blank=True
    )

    ip_lan = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    ip_publique = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    vlan = models.CharField(
        max_length=100,
        blank=True
    )

    domaine = models.CharField(
        max_length=200,
        blank=True
    )

    certificat_ssl = models.CharField(
        max_length=200,
        blank=True
    )

    systeme = models.CharField(
        max_length=200,
        blank=True
    )

    version_os = models.CharField(
        max_length=100,
        blank=True
    )

    serveur_application = models.CharField(
        max_length=200,
        blank=True
    )

    ip_serveur_application = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    cpu = models.CharField(
        max_length=50,
        blank=True
    )

    ram = models.CharField(
        max_length=50,
        blank=True
    )

    type_sgbd = models.CharField(
        max_length=100,
        blank=True
    )

    version_sgbd = models.CharField(
        max_length=50,
        blank=True
    )

    serveur_bd_dedie = models.BooleanField(
        default=False
    )

    ip_serveur_bd = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    nom_serveur_bd = models.CharField(
        max_length=200,
        blank=True
    )

    def clean(self):
        erreurs = {}

        if self.type_infrastructure == self.TypeInfrastructure.CLOUD:
            if not self.type_cloud:
                erreurs["type_cloud"] = (
                    "Le type de Cloud est obligatoire."
                )

        if self.type_infrastructure == self.TypeInfrastructure.ON_PREMISE:
            self.type_cloud = None

        if self.serveur_bd_dedie:
            if not self.ip_serveur_bd:
                erreurs["ip_serveur_bd"] = (
                    "L'adresse IP est obligatoire."
                )

            if not self.nom_serveur_bd:
                erreurs["nom_serveur_bd"] = (
                    "Le nom du serveur est obligatoire."
                )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Infrastructure - {self.fiche.nom_application}"
