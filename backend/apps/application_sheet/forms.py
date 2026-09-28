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

    # canaux_acces est un JSONField dans le modèle, mais correspond en
    # réalité à un choix fermé (UtilisateurAcces.Canal). On le déclare
    # explicitement ici pour obtenir des cases à cocher plutôt que le
    # widget Textarea par défaut d'un JSONField, qui obligerait
    # l'utilisateur à saisir du JSON à la main.
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
                "rows": 3
            }),
            "profils_utilisateurs": forms.Textarea(attrs={
                "rows": 3
            }),
        }


class DeveloppementForm(forms.ModelForm):

    # environnements est un JSONField adossé à Developpement.Environnement :
    # même correctif que pour canaux_acces ci-dessus.
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

    # emplacements est un JSONField adossé à Stockage.Emplacement :
    # même correctif que pour canaux_acces ci-dessus.
    emplacements = forms.MultipleChoiceField(
        choices=Stockage.Emplacement.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Emplacements",
    )

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
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        self.fiche = FicheApplicativeForm(
            *args,
            prefix="fiche",
            instance=instance
        )

        def get_related(name):
            if instance:
                # Need to handle related objects correctly. If it's a related manager (e.g., intervention is a ForeignKey to fiche), 
                # we just take the first one or a specific one for form editing?
                # Actually, related_name might be a OneToOneField or a ForeignKey. Let's assume OneToOne or we just take the first.
                manager_or_obj = getattr(instance, name, None)
                if manager_or_obj:
                    # If it's a manager (e.g. from ForeignKey)
                    if hasattr(manager_or_obj, 'first'):
                        return manager_or_obj.first()
                    # If it's a OneToOne
                    return manager_or_obj
            return None

        self.contrat = ContratForm(
            *args,
            prefix="contrat",
            instance=get_related("contrat")
        )

        self.infrastructure = InfrastructureForm(
            *args,
            prefix="infrastructure",
            instance=get_related("infrastructure")
        )

        self.acces = UtilisateurAccesForm(
            *args,
            prefix="acces",
            instance=get_related("acces")
        )

        self.developpement = DeveloppementForm(
            *args,
            prefix="developpement",
            instance=get_related("developpement")
        )

        self.module_metier = ModuleMetierForm(
            *args,
            prefix="module_metier",
            instance=get_related("module_metier")
        )

        self.stockage = StockageForm(
            *args,
            prefix="stockage",
            instance=get_related("stockage")
        )

        self.integration = IntegrationForm(
            *args,
            prefix="integration",
            instance=get_related("integration")
        )

        self.flux = FluxApplicationForm(
            *args,
            prefix="flux",
            instance=get_related("flux_application")
        )

        self.sauvegarde = SauvegardeForm(
            *args,
            prefix="sauvegarde",
            instance=get_related("sauvegarde")
        )

        self.intervention = InterventionForm(
            *args,
            prefix="intervention",
            instance=get_related("intervention")
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