from django import forms

from .models import Lieu, Reunion, Participation


class LieuForm(forms.ModelForm):

    class Meta:
        model = Lieu
        fields = [
            "nom_salle",
            "capacite",
        ]


class ReunionForm(forms.ModelForm):

    class Meta:
        model = Reunion
        fields = [
            "objet",
            "description",
            "date",
            "heure_debut",
            "heure_fin",
            "type",
            "statut",
            "organisateur",
            "lieu",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "heure_debut": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),
            "heure_fin": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }


class ParticipationForm(forms.ModelForm):

    class Meta:
        model = Participation
        fields = [
            "participant",
            "role",
            "statut",
        ]