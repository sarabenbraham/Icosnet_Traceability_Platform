from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

from apps.organization.models import Departement, Direction
from apps.users.models import ChefDepartement, Directeur, Ingenieur
from .models import Compte


User = get_user_model()

CLASSES_PAR_POSTE = {
    "directeur": Directeur,
    "chefdepartement": ChefDepartement,
    "ingenieur": Ingenieur,
    
}

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        compte = getattr(user, "compte", None)
        if compte is None:  # ex. superuser sans Compte
            return

        compte.verifier_expiration()
        if compte.expire or compte.statut != Compte.Statut.ACTIF:
            raise forms.ValidationError(
                "Ce compte est désactivé ou expiré.",
                code="compte_inactif",
            )

        
class CompteForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom", max_length=100, required=False)
    last_name = forms.CharField(label="Nom", max_length=100, required=False)
    email = forms.EmailField(label="Email professionnel", required=False)
    poste = forms.CharField(label="Poste / Fonction", max_length=100, required=False)
    est_helpdesk = forms.BooleanField(
        label="Rôle Agent Help Desk",
        required=False,
        help_text="Cocher si cet ingénieur peut traiter les tickets Help Desk.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Compte
        fields = [
            "email_connexion",
            "date_expiration",
            "expire",
            "statut",
        ]
        labels = {
            "email_connexion": "Email de connexion DSI",
            "date_expiration": "Date d'expiration",
            "statut": "Statut du compte",
            "expire": "Marquer comme expiré",
        }
        widgets = {
            "date_expiration": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.utilisateur:
            u = self.instance.utilisateur
            self.fields["first_name"].initial = u.first_name
            self.fields["last_name"].initial = u.last_name
            self.fields["email"].initial = u.email
            self.fields["poste"].initial = getattr(u, "poste", "")
            if hasattr(u, "ingenieur"):
                self.fields["est_helpdesk"].initial = u.ingenieur.est_helpdesk
            elif hasattr(u, "est_helpdesk"):
                self.fields["est_helpdesk"].initial = u.est_helpdesk

    def save(self, commit=True):
        compte = super().save(commit=False)

        # Mettre à jour l'utilisateur associé (Nom, Prénom, Email, Poste)
        if compte.utilisateur:
            u = compte.utilisateur
            if self.cleaned_data.get("first_name"):
                u.first_name = self.cleaned_data["first_name"]
            if self.cleaned_data.get("last_name"):
                u.last_name = self.cleaned_data["last_name"]
            if self.cleaned_data.get("email"):
                u.email = self.cleaned_data["email"]
            if self.cleaned_data.get("poste") is not None and hasattr(u, "poste"):
                u.poste = self.cleaned_data["poste"]

            u.save()

            if hasattr(u, "ingenieur"):
                ing = u.ingenieur
                ing.est_helpdesk = self.cleaned_data.get("est_helpdesk", False)
                ing.save(update_fields=["est_helpdesk"])
            elif hasattr(u, "est_helpdesk"):
                u.est_helpdesk = self.cleaned_data.get("est_helpdesk", False)
                u.save(update_fields=["est_helpdesk"])

        if commit:
            compte.save()

        return compte


class UtilisateurCompteForm(forms.ModelForm):
    poste = forms.ChoiceField(
        choices=[
            ("directeur", "Directeur"),
            ("chefdepartement", "Chef de département"),
            ("ingenieur", "Ingénieur"),
        ]
    )
    direction = forms.ModelChoiceField(
        queryset=Direction.objects.all(), required=False
    )
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(), required=False
    )
    email_connexion = forms.EmailField(required=True)
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, required=True)
    est_helpdesk = forms.BooleanField(
        required=False,
        label="R\u00f4le Agent Help Desk",
        help_text="Cocher si cet ing\u00e9nieur peut traiter les tickets Help Desk.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    date_expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "poste"]

    @transaction.atomic
    def save(self, commit=True):
        cd = self.cleaned_data
        classe = CLASSES_PAR_POSTE[cd["poste"]]

        utilisateur = classe(
            username=cd["username"],
            first_name=cd["first_name"],
            last_name=cd["last_name"],
            email=cd["email"],
            poste=cd["poste"],
        )
        utilisateur.set_password(cd["mot_de_passe"])
        utilisateur.save()

        # Lien avec l'organisation
        if classe is Directeur:
            direction = cd["direction"]
            direction.directeur = utilisateur
            direction.save(update_fields=["directeur"])
        elif classe is ChefDepartement:
            dep = cd["departement"]
            dep.chef_departement = utilisateur
            dep.save(update_fields=["chef_departement"])
        elif classe is Ingenieur:
            utilisateur.departement = cd["departement"]
            utilisateur.est_helpdesk = cd.get("est_helpdesk", False)
            utilisateur.save(update_fields=["departement", "est_helpdesk"])

        compte = Compte(
            utilisateur=utilisateur,
            email_connexion=cd["email_connexion"],
            date_expiration=cd["date_expiration"],
        )
        compte.set_password(cd["mot_de_passe"])
        compte.save()

        return utilisateur