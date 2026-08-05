from django.core.exceptions import ValidationError

from django.db import models


class FicheApplicative(models.Model):

    DOMAINE_CHOICES = [
        ("RH", "RH"),
        ("COMMERCIAL", "Commercial"),
        ("TECHNIQUE", "Technique / Telco"),
        ("MIDDLEWARE", "Middleware"),
        ("BI", "Décisionnel"),
    ]

    CRITICITE_CHOICES = [
        ("CRITIQUE", "Critique"),
        ("MAJEURE", "Majeure"),
        ("MINEURE", "Mineure"),
    ]

    STATUT_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("EN_ATTENTE", "En attente"),
        ("EN_VALIDATION", "En validation"),
        ("VALIDEE", "Validée"),
        ("REFUSEE", "Refusée"),
    ]

    nom_application = models.CharField(max_length=200)

    code_application = models.CharField(
        max_length=50,
        unique=True
    )

    domaine_fonctionnel = models.CharField(
        max_length=30,
        choices=DOMAINE_CHOICES
    )

    criticite = models.CharField(
        max_length=20,
        choices=CRITICITE_CHOICES
    )

    description = models.TextField()

    date_creation = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="BROUILLON"
    )

    ingenieur = models.ForeignKey(
        "users.Ingenieur",
        on_delete=models.CASCADE,
        related_name="fiches"
    )

    departements = models.ManyToManyField(
        "organization.Departement",
        related_name="fiches"
    )

    def __str__(self):
        return self.nom_application


class Contrat(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="contrat"
    )

    fournisseur = models.CharField(max_length=200)

    budget_annuel = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    support_externe = models.BooleanField(default=False)

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
        return self.fournisseur


class Infrastructure(models.Model):

    TYPE_INFRASTRUCTURE_CHOICES = [
        ("ON_PREMISE", "On-Premise"),
        ("CLOUD", "Cloud"),
    ]

    TYPE_CLOUD_CHOICES = [
        ("IAAS", "IaaS"),
        ("PAAS", "PaaS"),
        ("SAAS", "SaaS"),
    ]

    VIRTUALISATION_CHOICES = [
        ("PROXMOX", "Proxmox"),
        ("VMWARE", "VMware"),
        ("DOCKER", "Docker / Kubernetes"),
        ("PHYSIQUE", "Serveur Physique"),
    ]

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="infrastructure"
    )

    # ===========================
    # 2. Infrastructure
    # ===========================

    type_infrastructure = models.CharField(
        max_length=20,
        choices=TYPE_INFRASTRUCTURE_CHOICES
    )

    type_cloud = models.CharField(
        max_length=10,
        choices=TYPE_CLOUD_CHOICES,
        null=True,
        blank=True
    )

    plateforme_virtualisation = models.CharField(
        max_length=30,
        choices=VIRTUALISATION_CHOICES
    )

    # ===========================
    # 2.1 Réseau / Système
    # ===========================

    cluster = models.CharField(max_length=200)

    machine = models.CharField(max_length=200)

    ip_lan = models.GenericIPAddressField()

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

    systeme = models.CharField(max_length=200)

    version_os = models.CharField(max_length=100)

    # ===========================
    # 2.2 Dimensionnement
    # ===========================

    serveur_application = models.CharField(
        max_length=200
    )

    ip_serveur_application = models.GenericIPAddressField()

    cpu = models.CharField(
        max_length=50,
        help_text="Ex: 8 vCPU"
    )

    ram = models.CharField(
        max_length=50,
        help_text="Ex: 16 Go"
    )

    type_sgbd = models.CharField(
        max_length=100
    )

    version_sgbd = models.CharField(
        max_length=50
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

    def __str__(self):
        return f"{self.fiche} - Infrastructure"

    def clean(self):
        erreurs = {}

        # Cloud
        if self.type_infrastructure == "CLOUD" and not self.type_cloud:
            erreurs["type_cloud"] = "Obligatoire pour une infrastructure Cloud."

        if self.type_infrastructure == "ON_PREMISE":
            self.type_cloud = None

        # Base de données dédiée
        if self.serveur_bd_dedie:
            if not self.ip_serveur_bd:
                erreurs["ip_serveur_bd"] = "L'adresse IP est obligatoire."

            if not self.nom_serveur_bd:
                erreurs["nom_serveur_bd"] = "Le nom du serveur est obligatoire."
        else:
            self.ip_serveur_bd = None
            self.nom_serveur_bd = ""

        if erreurs:
            raise ValidationError(erreurs)


class UtilisateurAcces(models.Model):

    CANAL_CHOICES = [
        ("WEB", "Navigateur Web"),
        ("API", "API"),
        ("MOBILE", "Application Mobile"),
        ("CLI", "Client Lourd"),
    ]

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="utilisateurs_acces"
    )

    utilisateurs_cibles = models.TextField()

    profils_utilisateurs = models.TextField()

    canaux_acces = models.JSONField(default=list)

    def __str__(self):
        return f"{self.fiche} - Accès Utilisateurs"

    def clean(self):
        if not self.utilisateurs_cibles:
            raise ValidationError(
                {"utilisateurs_cibles": "Vous devez préciser les utilisateurs cibles."}
            )

        if not self.canaux_acces:
            raise ValidationError(
                {"canaux_acces": "Au moins un canal d'accès doit être sélectionné."}
            )

        canaux_valides = [choix[0] for choix in self.CANAL_CHOICES]

        for canal in self.canaux_acces:
            if canal not in canaux_valides:
                raise ValidationError({
                    "canaux_acces": f"{canal} n'est pas un canal valide."
                })
        

    

class Developpement(models.Model):

    MODE_CHOICES = [
        ("INTERNE", "Développé en interne"),
        ("EXTERNE", "Éditeur externe"),
    ]

    ENVIRONNEMENT_CHOICES = [
        ("PRODUCTION", "Production"),
        ("PREPROD", "Pré-production"),
        ("DEVELOPPEMENT", "Développement"),
    ]

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="developpement"
    )

    mode_developpement = models.CharField(
        max_length=20,
        choices=MODE_CHOICES
    )

    gestion_sources = models.CharField(max_length=300)

    processus_ci_cd = models.TextField()

    environnements = models.JSONField(default=list)

    methode_personnalisation = models.TextField()

    livrables_personnalisation = models.TextField()

    services = models.TextField()

    def __str__(self):
        return f"{self.fiche} - Développement"

    def clean(self):
        erreurs = {}

        if self.mode_developpement == "INTERNE" and not self.gestion_sources:
            erreurs["gestion_sources"] = (
                "Un dépôt Git est obligatoire pour un développement interne."
            )

        if not self.environnements:
            erreurs["environnements"] = (
                "Sélectionnez au moins un environnement."
            )

        valeurs_valides = [choix[0] for choix in self.ENVIRONNEMENT_CHOICES]

        for env in self.environnements:
            if env not in valeurs_valides:
                erreurs["environnements"] = (
                    f"{env} est un environnement invalide."
                )

        if erreurs:
            raise ValidationError(erreurs)



class ModuleMetier(models.Model):

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="modules"
    )

    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

    def clean(self):
        if not self.nom:
            raise ValidationError(
                {"nom": "Le nom du module est obligatoire."}
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fiche", "nom"],
                name="unique_module_par_fiche"
            )
        ]


class Stockage(models.Model):

    EMPLACEMENT_CHOICES = [
        ("LOCAL_VM", "Local VM"),
        ("NAS", "NAS"),
        ("OBJET", "Stockage Objet"),
        ("GED", "GED Externe"),
    ]

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="stockage"
    )

    persistance = models.BooleanField(default=False)

    emplacements = models.JSONField(default=list)

    def __str__(self):
        return f"{self.fiche} - Stockage"

    def clean(self):
        if self.persistance and not self.emplacements:
            raise ValidationError(
                {"emplacements": "Au moins un emplacement doit être sélectionné."}
            )

        if not self.persistance:
            self.emplacements = []

        emplacements_valides = [
    choix[0] for choix in self.EMPLACEMENT_CHOICES
]

        for emplacement in self.emplacements:
            if emplacement not in emplacements_valides:
                raise ValidationError({
                    "emplacements":
                    f"{emplacement} n'est pas un emplacement valide."
                })

class Integration(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="integration"
    )

    active_directory = models.BooleanField(default=False)

    groupes_ad = models.TextField(blank=True)

    messagerie = models.CharField(max_length=200)

    compte_messagerie = models.CharField(max_length=200)

    usage = models.CharField(max_length=200)

    integration_bi = models.BooleanField(default=False)

    methode_bi = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.fiche} - Intégration"

    def clean(self):
        if self.active_directory and not self.groupes_ad:
            raise ValidationError(
                {"groupes_ad": "Les groupes Active Directory sont obligatoires."}
            )

        if self.integration_bi and not self.methode_bi:
            raise ValidationError(
                {"methode_bi": "La méthode d'intégration BI est obligatoire."}
            )

class FluxApplication(models.Model):

    TYPE_CHOICES = [
        ("API", "API REST"),
        ("WEBHOOK", "Webhook"),
        ("AUTRE", "Autre"),
    ]

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="flux"
    )

    solution_distante = models.CharField(max_length=200)

    adresse = models.CharField(max_length=200)

    port = models.IntegerField()

    reception = models.BooleanField(default=False)

    envoi = models.BooleanField(default=False)

    type_flux = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    description = models.TextField()

    def __str__(self):
        return f"{self.fiche} - {self.solution_distante}"

    def clean(self):
        if not self.adresse:
            raise ValidationError(
                {"adresse": "L'adresse IP ou l'URL est obligatoire."}
            )

        if self.port <= 0:
            raise ValidationError(
                {"port": "Le port doit être compris entre 1 et 65535."}
            )


class Sauvegarde(models.Model):

    fiche = models.OneToOneField(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="sauvegarde"
    )

    emplacement_logs = models.TextField()

    supervision = models.CharField(max_length=200)

    sauvegarde_planifiee = models.BooleanField(default=False)

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
        return f"{self.fiche} - {self.emplacement_logs}"

    def clean(self):
        if self.sauvegarde_planifiee:
            if not self.outil:
                raise ValidationError({
                    "outil": "L'outil de sauvegarde est obligatoire."
                })

            if not self.recurrence:
                raise ValidationError({
                    "recurrence": "La récurrence est obligatoire."
                })

            if not self.heure:
                raise ValidationError({
                    "heure": "L'heure de sauvegarde est obligatoire."
                })

            if not self.console_backup:
                raise ValidationError({
                    "console_backup": "La console de sauvegarde est obligatoire."
                })
        else:
            self.outil = ""
            self.recurrence = ""
            self.heure = None


class Intervention(models.Model):

    STATUT_CHOICES = [
        ("SUCCES", "Succès"),
        ("ECHEC", "Échec"),
        ("ROLLBACK", "Rollback"),
    ]

    fiche = models.ForeignKey(
        FicheApplicative,
        on_delete=models.CASCADE,
        related_name="interventions"
    )

    date_heure = models.DateTimeField()

    intervenant = models.CharField(max_length=200)

    type_intervention = models.CharField(max_length=200)

    description = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES
    )

    def __str__(self):
        return f"{self.date_heure} - {self.type_intervention}"

    def clean(self):
        if not self.date_heure:
            raise ValidationError({
                "date_heure": "La date et l'heure de l'intervention sont obligatoires."
            })

        if not self.intervenant:
            raise ValidationError({
                "intervenant": "L'intervenant est obligatoire."
            })

        if not self.type_intervention:
            raise ValidationError({
                "type_intervention": "Le type d'intervention est obligatoire."
            })

        if not self.description:
            raise ValidationError({
                "description": "La description de l'intervention est obligatoire."
            })

