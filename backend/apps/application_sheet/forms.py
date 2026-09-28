from django import forms

from .models import (
    FicheApplicative,
    Contrat,
    Infrastructure,
    UtilisateurAcces,
    Developpement,
    ModuleMetier,
    Stockage,
    Integration,
    FluxApplication,
    Sauvegarde,
    Intervention,
)


# ============================================================
# 1. FICHE APPLICATIVE
# ============================================================

class FicheApplicativeForm(forms.ModelForm):

    class Meta:
        model = FicheApplicative

        # code_application n'est PAS dans les fields :
        # il est généré automatiquement par le modèle.
        fields = [
            "nom_application",
            "domaine_fonctionnel",
            "criticite",
            "description",
            "ingenieur",
            "departements",
        ]

        widgets = {
            "domaine_fonctionnel": forms.CheckboxSelectMultiple(),

            "description": forms.Textarea(attrs={
                "rows": 4,
            }),

            "departements": forms.CheckboxSelectMultiple(),
        }


# ============================================================
# 2. CONTRAT
# ============================================================

class ContratForm(forms.ModelForm):

    class Meta:
        model = Contrat
        exclude = ["fiche"]

        widgets = {
            "date_debut": forms.DateInput(
                attrs={"type": "date"}
            ),

            "date_fin": forms.DateInput(
                attrs={"type": "date"}
            ),

            "budget_annuel": forms.NumberInput(
                attrs={"step": "0.01"}
            ),
        }


# ============================================================
# 3. INFRASTRUCTURE
# ============================================================

class InfrastructureForm(forms.ModelForm):

    class Meta:
        model = Infrastructure
        exclude = ["fiche"]

        widgets = {
            "ip_lan": forms.TextInput(),
            "ip_publique": forms.TextInput(),
            "ip_serveur_application": forms.TextInput(),
            "ip_serveur_bd": forms.TextInput(),
        }


# ============================================================
# 4. UTILISATEURS & ACCÈS
# ============================================================

class UtilisateurAccesForm(forms.ModelForm):

    canaux_acces = forms.MultipleChoiceField(
        choices=UtilisateurAcces.Canal.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Canaux d'accès",
    )

    class Meta:
        model = UtilisateurAcces
        exclude = ["fiche"]

        widgets = {
            "utilisateurs_cibles": forms.Textarea(attrs={
                "rows": 3,
            }),

            "profils_utilisateurs": forms.Textarea(attrs={
                "rows": 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # JSONField -> liste pour les cases à cocher
        if self.instance and self.instance.pk:
            self.fields["canaux_acces"].initial = (
                self.instance.canaux_acces or []
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Liste des cases cochées -> JSONField
        instance.canaux_acces = self.cleaned_data.get(
            "canaux_acces",
            []
        )

        if commit:
            instance.save()

        return instance


# ============================================================
# 5. DÉVELOPPEMENT
# ============================================================

class DeveloppementForm(forms.ModelForm):

    environnements = forms.MultipleChoiceField(
        choices=Developpement.Environnement.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Environnements",
    )

    class Meta:
        model = Developpement
        exclude = ["fiche"]

        widgets = {
            "processus_ci_cd": forms.Textarea(attrs={
                "rows": 3,
            }),

            "methode_personnalisation": forms.Textarea(attrs={
                "rows": 3,
            }),

            "livrables_personnalisation": forms.Textarea(attrs={
                "rows": 3,
            }),

            "services": forms.Textarea(attrs={
                "rows": 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["environnements"].initial = (
                self.instance.environnements or []
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.environnements = self.cleaned_data.get(
            "environnements",
            []
        )

        if commit:
            instance.save()

        return instance


# ============================================================
# 6. MODULES MÉTIER
# ============================================================

class ModuleMetierForm(forms.ModelForm):

    class Meta:
        model = ModuleMetier
        exclude = ["fiche"]

        widgets = {
            "modules": forms.Textarea(attrs={
                "rows": 4,
            }),

            "description": forms.Textarea(attrs={
                "rows": 3,
            }),
        }


# ============================================================
# 7. STOCKAGE
# ============================================================

class StockageForm(forms.ModelForm):

    emplacements = forms.MultipleChoiceField(
        choices=Stockage.Emplacement.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Emplacements",
    )

    class Meta:
        model = Stockage
        exclude = ["fiche"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["emplacements"].initial = (
                self.instance.emplacements or []
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.emplacements = self.cleaned_data.get(
            "emplacements",
            []
        )

        if commit:
            instance.save()

        return instance


# ============================================================
# 8. INTÉGRATION
# ============================================================

class IntegrationForm(forms.ModelForm):

    class Meta:
        model = Integration
        exclude = ["fiche"]

        widgets = {
            "groupes_ad": forms.Textarea(attrs={
                "rows": 3,
            }),
        }


# ============================================================
# 9. FLUX APPLICATION
# ============================================================

class FluxApplicationForm(forms.ModelForm):

    class Meta:
        model = FluxApplication
        exclude = ["fiche"]


# ============================================================
# 10. SAUVEGARDE / SUPERVISION
# ============================================================

class SauvegardeForm(forms.ModelForm):

    class Meta:
        model = Sauvegarde
        exclude = ["fiche"]

        widgets = {
            "emplacement_logs": forms.Textarea(attrs={
                "rows": 3,
            }),

            "heure": forms.TimeInput(attrs={
                "type": "time",
            }),
        }


# ============================================================
# 11. INTERVENTION
# ============================================================

class InterventionForm(forms.ModelForm):

    class Meta:
        model = Intervention
        exclude = ["fiche"]

        widgets = {
            "date_heure": forms.DateTimeInput(attrs={
                "type": "datetime-local",
            }),

            "description": forms.Textarea(attrs={
                "rows": 4,
            }),
        }


# ============================================================
# FORMULAIRE COMPLET
# ============================================================

class FicheApplicativeCompleteForm(forms.Form):

    def __init__(self, *args, **kwargs):

        instance = kwargs.pop("instance", None)

        super().__init__(*args, **kwargs)

        self.instance = instance

        # --------------------------------------------------------
        # Fiche principale
        # --------------------------------------------------------

        self.fiche = FicheApplicativeForm(
            *args,
            prefix="fiche",
            instance=instance,
        )

        # --------------------------------------------------------
        # Fonction pour récupérer les OneToOne
        # --------------------------------------------------------

        def get_related(name):

            if not instance:
                return None

            try:
                return getattr(instance, name)
            except Exception:
                return None

        # --------------------------------------------------------
        # Sections
        # --------------------------------------------------------

        self.contrat = ContratForm(
            *args,
            prefix="contrat",
            instance=get_related("contrat"),
        )

        self.infrastructure = InfrastructureForm(
            *args,
            prefix="infrastructure",
            instance=get_related("infrastructure"),
        )

        self.acces = UtilisateurAccesForm(
            *args,
            prefix="acces",
            instance=get_related("acces"),
        )

        self.developpement = DeveloppementForm(
            *args,
            prefix="developpement",
            instance=get_related("developpement"),
        )

        self.module_metier = ModuleMetierForm(
            *args,
            prefix="module_metier",
            instance=get_related("module_metier"),
        )

        self.stockage = StockageForm(
            *args,
            prefix="stockage",
            instance=get_related("stockage"),
        )

        self.integration = IntegrationForm(
            *args,
            prefix="integration",
            instance=get_related("integration"),
        )

        self.flux = FluxApplicationForm(
            *args,
            prefix="flux",
            instance=get_related("flux_application"),
        )

        self.sauvegarde = SauvegardeForm(
            *args,
            prefix="sauvegarde",
            instance=get_related("sauvegarde"),
        )

        self.intervention = InterventionForm(
            *args,
            prefix="intervention",
            instance=get_related("intervention"),
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    def is_valid(self):

        return all([
            self.fiche.is_valid(),
            self.contrat.is_valid(),
            self.infrastructure.is_valid(),
            self.acces.is_valid(),
            self.developpement.is_valid(),
            self.module_metier.is_valid(),
            self.stockage.is_valid(),
            self.integration.is_valid(),
            self.flux.is_valid(),
            self.sauvegarde.is_valid(),
            self.intervention.is_valid(),
        ])

    # ============================================================
    # SAUVEGARDE COMPLÈTE
    # ============================================================

    def save(self):

        # --------------------------------------------------------
        # 1. Fiche principale
        # --------------------------------------------------------

        fiche = self.fiche.save(commit=False)

        fiche.save()

        # Important pour ManyToMany "departements"
        self.fiche.save_m2m()

        # --------------------------------------------------------
        # 2. Sections OneToOne
        # --------------------------------------------------------

        contrat = self.contrat.save(commit=False)
        contrat.fiche = fiche
        contrat.save()

        infrastructure = self.infrastructure.save(commit=False)
        infrastructure.fiche = fiche
        infrastructure.save()

        acces = self.acces.save(commit=False)
        acces.fiche = fiche
        acces.save()

        developpement = self.developpement.save(commit=False)
        developpement.fiche = fiche
        developpement.save()

        module_metier = self.module_metier.save(commit=False)
        module_metier.fiche = fiche
        module_metier.save()

        stockage = self.stockage.save(commit=False)
        stockage.fiche = fiche
        stockage.save()

        integration = self.integration.save(commit=False)
        integration.fiche = fiche
        integration.save()

        flux = self.flux.save(commit=False)
        flux.fiche = fiche
        flux.save()

        sauvegarde = self.sauvegarde.save(commit=False)
        sauvegarde.fiche = fiche
        sauvegarde.save()

        intervention = self.intervention.save(commit=False)
        intervention.fiche = fiche
        intervention.save()

        return fiche