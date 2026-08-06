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

        exclude = [
            "date_creation",
            "statut",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "departements": forms.CheckboxSelectMultiple(),
        }


class ContratForm(forms.ModelForm):

    class Meta:
        model = Contrat

        exclude = [
            "fiche",
        ]

        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}),
            "date_fin": forms.DateInput(attrs={"type": "date"}),
        }


class InfrastructureForm(forms.ModelForm):

    class Meta:
        model = Infrastructure

        exclude = [
            "fiche",
        ]

        widgets = {
            "certificat_ssl": forms.Textarea(attrs={"rows": 2}),
        }


class UtilisateurAccesForm(forms.ModelForm):

    canaux_acces = forms.MultipleChoiceField(
        choices=UtilisateurAcces.CANAL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = UtilisateurAcces

        exclude = [
            "fiche",
        ]



class DeveloppementForm(forms.ModelForm):

    environnements = forms.MultipleChoiceField(
        choices=Developpement.ENVIRONNEMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Developpement

        exclude = [
            "fiche",
        ]

        widgets = {
            "processus_ci_cd": forms.Textarea(attrs={"rows": 3}),
            "methode_personnalisation": forms.Textarea(attrs={"rows": 3}),
            "livrables_personnalisation": forms.Textarea(attrs={"rows": 3}),
            "services": forms.Textarea(attrs={"rows": 3}),
        }


class ModuleMetierForm(forms.ModelForm):

    class Meta:
        model = ModuleMetier

        exclude = [
            "fiche",
        ]


class StockageForm(forms.ModelForm):

    emplacements = forms.MultipleChoiceField(
        choices=Stockage.EMPLACEMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Stockage

        exclude = [
            "fiche",
        ]


class IntegrationForm(forms.ModelForm):

    class Meta:
        model = Integration

        exclude = [
            "fiche",
        ]

        widgets = {
            "groupes_ad": forms.Textarea(attrs={"rows": 3}),
        }


class FluxApplicationForm(forms.ModelForm):

    class Meta:
        model = FluxApplication

        exclude = [
            "fiche",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class SauvegardeForm(forms.ModelForm):

    class Meta:
        model = Sauvegarde

        exclude = [
            "fiche",
        ]

        widgets = {
            "emplacement_logs": forms.Textarea(attrs={"rows": 3}),
            "heure": forms.TimeInput(attrs={"type": "time"}),
        }


class InterventionForm(forms.ModelForm):

    class Meta:
        model = Intervention

        exclude = [
            "fiche",
        ]

        widgets = {
            "date_heure": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }