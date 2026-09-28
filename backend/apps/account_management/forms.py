from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

from .models import Compte


User = get_user_model()


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

    email_connexion = forms.EmailField(
        required=True,
    )

    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
    )

    date_expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "poste",
        ]

    @transaction.atomic
    def save(self, commit=True):
        utilisateur = super().save(commit=False)

        utilisateur.set_password(
            self.cleaned_data["mot_de_passe"]
        )

        if commit:
            utilisateur.save()

            compte = Compte(
                utilisateur=utilisateur,
                email_connexion=self.cleaned_data["email_connexion"],
                date_expiration=self.cleaned_data["date_expiration"],
            )

            compte.set_password(
                self.cleaned_data["mot_de_passe"]
            )

            compte.save()

        return utilisateur