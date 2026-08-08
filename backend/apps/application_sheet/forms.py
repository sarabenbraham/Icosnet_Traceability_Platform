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


class FicheApplicativeForm(forms.ModelForm):

    class Meta:
        model = FicheApplicative
        fields = [
            "nom_application",
            "code_application",
            "domaine_fonctionnel",
            "criticite",
            "description",
            "ingenieur",
            "departements",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4
            }),
            "departements": forms.CheckboxSelectMultiple(),
        }


class ContratForm(forms.ModelForm):

    class Meta:
        model = Contrat
        exclude = ["fiche"]


class InfrastructureForm(forms.ModelForm):

    class Meta:
        model = Infrastructure
        exclude = ["fiche"]


class UtilisateurAccesForm(forms.ModelForm):

    class Meta:
        model = UtilisateurAcces
        exclude = ["fiche"]

        widgets = {
            "utilisateurs_cibles": forms.Textarea(attrs={
                "rows": 3
            }),
            "profils_utilisateurs": forms.Textarea(attrs={
                "rows": 3
            }),
        }


class DeveloppementForm(forms.ModelForm):

    class Meta:
        model = Developpement
        exclude = ["fiche"]

        widgets = {
            "processus_ci_cd": forms.Textarea(attrs={
                "rows": 3
            }),
            "methode_personnalisation": forms.Textarea(attrs={
                "rows": 3
            }),
            "livrables_personnalisation": forms.Textarea(attrs={
                "rows": 3
            }),
            "services": forms.Textarea(attrs={
                "rows": 3
            }),
        }


class ModuleMetierForm(forms.ModelForm):

    class Meta:
        model = ModuleMetier
        exclude = ["fiche"]

        widgets = {
            "modules": forms.Textarea(attrs={
                "rows": 4
            }),
            "description": forms.Textarea(attrs={
                "rows": 3
            }),
        }


class StockageForm(forms.ModelForm):

    class Meta:
        model = Stockage
        exclude = ["fiche"]


class IntegrationForm(forms.ModelForm):

    class Meta:
        model = Integration
        exclude = ["fiche"]

        widgets = {
            "groupes_ad": forms.Textarea(attrs={
                "rows": 3
            }),
        }


class FluxApplicationForm(forms.ModelForm):

    class Meta:
        model = FluxApplication
        exclude = ["fiche"]


class SauvegardeForm(forms.ModelForm):

    class Meta:
        model = Sauvegarde
        exclude = ["fiche"]


class InterventionForm(forms.ModelForm):

    class Meta:
        model = Intervention
        exclude = ["fiche"]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4
            }),
        }


class FicheApplicativeCompleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fiche = FicheApplicativeForm(
            *args,
            prefix="fiche"
        )

        self.contrat = ContratForm(
            *args,
            prefix="contrat"
        )

        self.infrastructure = InfrastructureForm(
            *args,
            prefix="infrastructure"
        )

        self.acces = UtilisateurAccesForm(
            *args,
            prefix="acces"
        )

        self.developpement = DeveloppementForm(
            *args,
            prefix="developpement"
        )

        self.module_metier = ModuleMetierForm(
            *args,
            prefix="module_metier"
        )

        self.stockage = StockageForm(
            *args,
            prefix="stockage"
        )

        self.integration = IntegrationForm(
            *args,
            prefix="integration"
        )

        self.flux = FluxApplicationForm(
            *args,
            prefix="flux"
        )

        self.sauvegarde = SauvegardeForm(
            *args,
            prefix="sauvegarde"
        )

        self.intervention = InterventionForm(
            *args,
            prefix="intervention"
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