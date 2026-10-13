from django import forms
from django.forms import inlineformset_factory

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
            "departements",
        ]

        widgets = {
            "domaine_fonctionnel": forms.CheckboxSelectMultiple(),

            "description": forms.Textarea(attrs={
                "rows": 4,
            }),

            "departements": forms.CheckboxSelectMultiple(),
        }


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


class ModuleMetierForm(forms.ModelForm):

    class Meta:
        model = ModuleMetier
        exclude = ["fiche", "modules"]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 3,
            }),
        }

    def get_modules(self):
        """Liste des modules à afficher dans le formulaire."""
        if self.is_bound:
            # Après envoi du formulaire : valeurs saisies
            valeurs = self.data.getlist(f"{self.prefix}-module")
        elif self.instance and self.instance.pk:
            # Modification : valeurs enregistrées
            valeurs = self.instance.modules or []
        else:
            valeurs = []

        return [v.strip() for v in valeurs if v.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.modules = self.get_modules()

        if commit:
            instance.save()

        return instance


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


class IntegrationForm(forms.ModelForm):

    class Meta:
        model = Integration
        exclude = ["fiche"]

        widgets = {
            "groupes_ad": forms.Textarea(attrs={
                "rows": 3,
            }),
        }


FluxFormSet = inlineformset_factory(
    FicheApplicative,
    FluxApplication,
    fields=[
        "solution_distante",
        "adresse",
        "port",
        "sens",
        "type_flux",
        "description",
    ],
    widgets={
        "description": forms.Textarea(attrs={"rows": 1}),
        "port": forms.NumberInput(attrs={"min": 1, "max": 65535}),
    },
    extra=1,
    can_delete=True,
)


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


InterventionFormSet = inlineformset_factory(
    FicheApplicative,
    Intervention,
    fields=[
        "date_heure",
        "intervenant",
        "type_intervention",
        "description",
        "statut",
    ],
    widgets={
        "date_heure": forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        "description": forms.Textarea(attrs={"rows": 1}),
    },
    extra=1,
    can_delete=True,
)

class FicheApplicativeCompleteForm(forms.Form):

    def __init__(self, *args, **kwargs):

        instance = kwargs.pop("instance", None)

        super().__init__(*args, **kwargs)

        self.instance = instance


        self.fiche = FicheApplicativeForm(
            *args,
            prefix="fiche",
            instance=instance,
        )

        def get_related(name):

            if not instance:
                return None

            try:
                return getattr(instance, name)
            except Exception:
                return None


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

        data = args[0] if args else None

        self.flux = FluxFormSet(
            data,
            instance=instance,
            prefix="flux",
        )

        self.sauvegarde = SauvegardeForm(
            *args,
            prefix="sauvegarde",
            instance=get_related("sauvegarde"),
        )

        self.intervention = InterventionFormSet(
            data,
            instance=instance,
            prefix="intervention",
        )


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