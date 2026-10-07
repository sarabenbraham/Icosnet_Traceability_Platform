from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from .models import Lieu, Reunion, ProcesVerbal, nom_complet

User = get_user_model()

TAILLE_MAX_PV = 10 * 1024 * 1024  # 10 Mo


class StyledFormMixin:
    """Applique la classe CSS form-input à tous les champs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                field.widget.attrs.setdefault("class", "form-input")


class LieuForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Lieu
        fields = ["nom_salle", "places_illimitees", "capacite"]
        labels = {"nom_salle": "Nom du lieu"}


class ReunionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ["objet", "description", "date", "heure_debut", "heure_fin",
                  "type", "organisateur", "lieu"]
        labels = {"lieu": "Lieu"}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lieu"].required = False
        self.fields["lieu"].empty_label = "— Aucun lieu —"


class ParticipationForm(StyledFormMixin, forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Sélectionner des utilisateurs",
    )
    externes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Un nom ou un email par ligne"}),
        label="Participants externes (facultatif)",
    )
    role = forms.CharField(required=False, max_length=100, label="Rôle dans la réunion")

    def __init__(self, *args, reunion=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = User.objects.filter(is_active=True).order_by("last_name", "first_name", "username")
        if reunion is not None:
            # On ne propose pas les utilisateurs déjà invités
            qs = qs.exclude(participations_reunions__reunion=reunion)
        self.fields["participants"].queryset = qs
        self.fields["participants"].label_from_instance = nom_complet


class PVForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ProcesVerbal
        fields = ["contenu", "resultats", "document"]
        widgets = {
            "contenu": forms.Textarea(attrs={"rows": 8}),
            "resultats": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_document(self):
        fichier = self.cleaned_data.get("document")
        if isinstance(fichier, UploadedFile) and fichier.size > TAILLE_MAX_PV:
            raise ValidationError("Le fichier dépasse 10 Mo.")
        return fichier