from django import forms
from .models import Ticket, Commentaire


class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = ["titre", "categorie", "priorite", "description"]
        widgets = {
            "titre": forms.TextInput(attrs={
                "placeholder": "R\u00e9sumer le probl\u00e8me en une ligne\u2026",
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "D\u00e9crivez le probl\u00e8me en d\u00e9tail\u2026",
                "rows": 5,
                "class": "form-control",
            }),
            "categorie": forms.Select(attrs={"class": "form-control"}),
            "priorite":  forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "titre":       "Titre du probl\u00e8me",
            "categorie":   "Cat\u00e9gorie",
            "priorite":    "Priorit\u00e9",
            "description": "Description d\u00e9taill\u00e9e",
        }


class StatutForm(forms.ModelForm):
    """Formulaire pour que l'ing\u00e9nieur change le statut et s'assigne."""
    class Meta:
        model  = Ticket
        fields = ["statut", "assigne_a"]
        widgets = {
            "statut":     forms.Select(attrs={"class": "form-control"}),
            "assigne_a":  forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "statut":    "Statut",
            "assigne_a": "Ing\u00e9nieur assign\u00e9",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.users.models import Ingenieur
        self.fields["assigne_a"].queryset = Ingenieur.objects.filter(est_helpdesk=True)
        self.fields["assigne_a"].empty_label = "— Choisir un agent Help Desk —"
        self.fields["assigne_a"].required = False


class CommentaireForm(forms.ModelForm):
    class Meta:
        model  = Commentaire
        fields = ["contenu"]
        widgets = {
            "contenu": forms.Textarea(attrs={
                "placeholder": "Votre r\u00e9ponse ou commentaire\u2026",
                "rows": 3,
                "class": "form-control",
            }),
        }
        labels = {"contenu": ""}
