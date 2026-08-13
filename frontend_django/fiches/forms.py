from django import forms


DOMAINE_CHOICES = [
    ('', '-- Sélectionner un domaine --'),
    ('RH', 'RH'),
    ('COMMERCIAL', 'Commercial'),
    ('TECHNIQUE', 'Technique / Telco'),
    ('MIDDLEWARE', 'Middleware'),
    ('BI', 'Décisionnel'),
]

CRITICITE_CHOICES = [
    ('', '-- Sélectionner la criticité --'),
    ('CRITIQUE', 'Critique'),
    ('MAJEURE', 'Majeure'),
    ('MINEURE', 'Mineure'),
]

STATUT_CHOICES = [
    ('BROUILLON', 'Brouillon'),
    ('EN_ATTENTE', 'En attente'),
    ('EN_VALIDATION', 'En validation'),
    ('VALIDEE', 'Validée'),
    ('REFUSEE', 'Refusée'),
]


class FicheApplicativeForm(forms.Form):
    nom_application = forms.CharField(
        max_length=200,
        label='Nom de l\'application',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ex: ERP SAGE X3',
        })
    )
    code_application = forms.CharField(
        max_length=50,
        label='Code application',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ex: ERP-001',
        })
    )
    domaine_fonctionnel = forms.ChoiceField(
        choices=DOMAINE_CHOICES,
        label='Domaine fonctionnel',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    criticite = forms.ChoiceField(
        choices=CRITICITE_CHOICES,
        label='Criticité',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 4,
            'placeholder': 'Description fonctionnelle de l\'application...',
        })
    )
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        label='Statut',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
