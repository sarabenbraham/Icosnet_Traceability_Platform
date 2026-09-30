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

    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = Compte
        fields = [
            "utilisateur",
            "email_connexion",
            "mot_de_passe",
            "date_expiration",
            "expire",
            "statut",
        ]

        widgets = {
            "date_expiration": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def save(self, commit=True):
        compte = super().save(commit=False)

        mot_de_passe = self.cleaned_data.get("mot_de_passe")

        if mot_de_passe:
            compte.set_password(mot_de_passe)

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
    date_expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "poste"]

    def clean(self):
        cleaned = super().clean()
        poste = cleaned.get("poste")
        if poste == "directeur" and not cleaned.get("direction"):
            self.add_error("direction", "Choisis la direction de ce directeur.")
        if poste in ("chefdepartement", "ingenieur") and not cleaned.get("departement"):
            self.add_error("departement", "Choisis le département.")
        return cleaned

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
            utilisateur.save(update_fields=["departement"])

        compte = Compte(
            utilisateur=utilisateur,
            email_connexion=cd["email_connexion"],
            date_expiration=cd["date_expiration"],
        )
        compte.set_password(cd["mot_de_passe"])
        compte.save()

        return utilisateur