from django import forms

ROLE_CHOICES = [
    ('INGENIEUR', 'Ingénieur DSI'),
    ('CHEF_DEPARTEMENT', 'Chef de Département'),
    ('DIRECTEUR', 'Directeur DSI'),
]


class ConnexionForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur ou Email",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'ex: ahmed.benali@icosnet.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••••••',
        })
    )
    se_souvenir = forms.BooleanField(
        required=False,
        label="Se souvenir de moi",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class ProfilForm(forms.Form):
    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    poste = forms.CharField(
        label="Poste / Fonction",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ex: Ingénieur Systèmes & Réseaux'})
    )
    departement = forms.CharField(
        label="Département",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ex: Infrastructures & Cloud'})
    )


class UtilisateurForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ex: jdoe'})
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John'})
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Doe'})
    )
    email = forms.EmailField(
        label="Email professionnel",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'j.doe@icosnet.com'})
    )
    role = forms.ChoiceField(
        label="Rôle / Type d'utilisateur",
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    poste = forms.CharField(
        label="Poste",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ingénieur DSI'})
    )
