from django.core.exceptions import ValidationError
from django.db import models


class FicheApplicative(models.Model):

    class Domaine(models.TextChoices):
        RH = "RH", "RH"
        COMMERCIAL = "COMMERCIAL", "Commercial"
        TECHNIQUE = "TECHNIQUE", "Technique / Telco"
        MIDDLEWARE = "MIDDLEWARE", "Middleware"
        BI = "BI", "Décisionnel"

    class Criticite(models.TextChoices):
        CRITIQUE = "CRITIQUE", "Critique"
        MAJEURE = "MAJEURE", "Majeure"
        MINEURE = "MINEURE", "Mineure"

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", "Brouillon"
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        EN_VALIDATION = "EN_VALIDATION", "En validation"
        VALIDEE = "VALIDEE", "Validée"
        REFUSEE = "REFUSEE", "Refusée"

    nom_application = models.CharField(max_length=200)

    code_application = models.CharField(
        max_length=50,
        unique=True
    )

    domaine_fonctionnel = models.CharField(
        max_length=30,
        choices=Domaine.choices
    )

    criticite = models.CharField(
        max_length=20,
        choices=Criticite.choices
    )

    description = models.TextField(blank=True)

    ingenieur = models.ForeignKey(
        "users.Ingenieur",
        on_delete=models.PROTECT,
        related_name="fiches"
    )

    departements = models.ManyToManyField(
        "organization.Departement",
        related_name="fiches",
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.BROUILLON
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Fiche applicative"
        verbose_name_plural = "Fiches applicatives"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.nom_application} ({self.code_application})"


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


class Developpement(models.Model):

    class ModeDeveloppement(models.TextChoices):
        INTERNE = "INTERNE", "Développé en interne"
        EXTERNE = "EXTERNE", "Éditeur externe"

    class Environnement(models.TextChoices):
        PRODUCTION = "PRODUCTION", "Production"
        PREPROD = "PREPROD", "Pré-production"
        DEVELOPPEMENT = "DEVELOPPEMENT", "Développement"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="developpement"
    )

    mode_developpement = models.CharField(
        max_length=20,
        choices=ModeDeveloppement.choices
    )

    gestion_sources = models.CharField(
        max_length=300,
        blank=True
    )

    processus_ci_cd = models.TextField(
        blank=True
    )

    environnements = models.JSONField(
        default=list
    )

    methode_personnalisation = models.TextField(
        blank=True
    )

    livrables_personnalisation = models.TextField(
        blank=True
    )

    services = models.TextField(
        blank=True
    )

    def clean(self):
        erreurs = {}

        if (
            self.mode_developpement == self.ModeDeveloppement.INTERNE
            and not self.gestion_sources
        ):
            erreurs["gestion_sources"] = (
                "Un dépôt Git est obligatoire "
                "pour un développement interne."
            )

        if not self.environnements:
            erreurs["environnements"] = (
                "Sélectionnez au moins un environnement."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Développement - {self.fiche.nom_application}"


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


class Stockage(models.Model):

    class Emplacement(models.TextChoices):
        LOCAL_VM = "LOCAL_VM", "Local VM"
        NAS = "NAS", "NAS"
        OBJET = "OBJET", "Stockage Objet"
        GED = "GED", "GED Externe"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="stockage"
    )

    persistance = models.BooleanField(
        default=False
    )

    emplacements = models.JSONField(
        default=list
    )

    def clean(self):
        erreurs = {}

        if self.persistance and not self.emplacements:
            erreurs["emplacements"] = (
                "Au moins un emplacement est obligatoire."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Stockage - {self.fiche.nom_application}"



class Integration(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="integration"
    )

    active_directory = models.BooleanField(
        default=False
    )

    groupes_ad = models.TextField(
        blank=True
    )

    messagerie = models.CharField(
        max_length=200,
        blank=True
    )

    compte_messagerie = models.CharField(
        max_length=200,
        blank=True
    )

    usage = models.CharField(
        max_length=200,
        blank=True
    )

    integration_bi = models.BooleanField(
        default=False
    )

    methode_bi = models.CharField(
        max_length=200,
        blank=True
    )

    def clean(self):
        erreurs = {}

        if self.active_directory and not self.groupes_ad:
            erreurs["groupes_ad"] = (
                "Les groupes Active Directory sont obligatoires."
            )

        if self.integration_bi and not self.methode_bi:
            erreurs["methode_bi"] = (
                "La méthode d'intégration BI est obligatoire."
            )

        if erreurs:
            raise ValidationError(erreurs)

    def __str__(self):
        return f"Intégration - {self.fiche.nom_application}"


class FluxApplication(models.Model):

    class TypeFlux(models.TextChoices):
        API = "API", "API REST"
        WEBHOOK = "WEBHOOK", "Webhook"
        AUTRE = "AUTRE", "Autre"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="flux_application"
    )

    adresse = models.CharField(
        max_length=255,
        blank=True
    )

    port = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    type_flux = models.CharField(
        max_length=20,
        choices=TypeFlux.choices,
        blank=True
    )

    def clean(self):
        if self.port is not None and not (
            1 <= self.port <= 65535
        ):
            raise ValidationError({
                "port":
                "Le port doit être compris entre 1 et 65535."
            })

    def __str__(self):
        return f"Flux - {self.fiche.nom_application}"



class Sauvegarde(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="sauvegarde"
    )

    emplacement_logs = models.TextField(
        blank=True
    )

    supervision = models.CharField(
        max_length=200,
        blank=True
    )

    sauvegarde_planifiee = models.BooleanField(
        default=False
    )

    outil = models.CharField(
        max_length=200,
        blank=True
    )

    recurrence = models.CharField(
        max_length=100,
        blank=True
    )

    heure = models.TimeField(
        null=True,
        blank=True
    )

    console_backup = models.URLField(
        blank=True
    )

    def __str__(self):
        return f"Sauvegarde - {self.fiche.nom_application}"


class Intervention(models.Model):

    class StatutIntervention(models.TextChoices):
        SUCCES = "SUCCES", "Succès"
        ECHEC = "ECHEC", "Échec"
        ROLLBACK = "ROLLBACK", "Rollback"

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="intervention"
    )

    date_heure = models.DateTimeField(
        null=True,
        blank=True
    )

    intervenant = models.CharField(
        max_length=200,
        blank=True
    )

    type_intervention = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutIntervention.choices,
        blank=True
    )

    def __str__(self):
        return f"Intervention - {self.fiche.nom_application}"
    