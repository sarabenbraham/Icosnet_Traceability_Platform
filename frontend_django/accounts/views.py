from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConnexionForm, ProfilForm, UtilisateurForm

# Utilisateurs démo pour la gestion des comptes
UTILISATEURS_DEMO = [
    {
        'id': 1,
        'username': 'ahmed.benali',
        'first_name': 'Ahmed',
        'last_name': 'Benali',
        'email': 'ahmed.benali@icosnet.com',
        'role': 'INGENIEUR',
        'role_label': 'Ingénieur DSI',
        'poste': 'Ingénieur Systèmes & Réseaux',
        'departement': 'Infrastructures & Cloud',
        'statut': 'ACTIF',
    },
    {
        'id': 2,
        'username': 'karim.messaoud',
        'first_name': 'Karim',
        'last_name': 'Messaoud',
        'email': 'karim.messaoud@icosnet.com',
        'role': 'INGENIEUR',
        'role_label': 'Ingénieur DSI',
        'poste': 'Ingénieur Télécom & VoIP',
        'departement': 'Réseaux & Télécoms',
        'statut': 'ACTIF',
    },
    {
        'id': 3,
        'username': 'sara.benbraham',
        'first_name': 'Sara',
        'last_name': 'Benbraham',
        'email': 'sara.benbraham@icosnet.com',
        'role': 'CHEF_DEPARTEMENT',
        'role_label': 'Chef de Département',
        'poste': 'Chef de Département Développement',
        'departement': 'Développement & Solutions',
        'statut': 'ACTIF',
    },
    {
        'id': 4,
        'username': 'farah.laggoune',
        'first_name': 'Farah',
        'last_name': 'Laggoune',
        'email': 'farah.laggoune@icosnet.com',
        'role': 'DIRECTEUR',
        'role_label': 'Directeur DSI',
        'poste': 'Directeur des Systèmes d\'Information',
        'departement': 'Direction DSI',
        'statut': 'ACTIF',
    },
]


def connexion_view(request):
    """Vue de connexion / Login."""
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Bienvenue ! Connexion réussie en tant que {form.cleaned_data['username']}.")
            return redirect('dashboard:home')
    else:
        form = ConnexionForm()

    return render(request, 'accounts/login.html', {'form': form})


def deconnexion_view(request):
    """Déconnexion de l'utilisateur."""
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('accounts:login')


def profil_view(request):
    """Vue du profil utilisateur courant."""
    user_data = UTILISATEURS_DEMO[0]  # Ahmed Benali par défaut

    if request.method == 'POST':
        form = ProfilForm(request.POST)
        if form.is_valid():
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('accounts:profil')
    else:
        form = ProfilForm(initial=user_data)

    return render(request, 'accounts/profil.html', {
        'form': form,
        'user_data': user_data,
    })


def utilisateurs_liste_view(request):
    """Liste de tous les comptes utilisateurs DSI."""
    query = request.GET.get('q', '')
    utilisateurs = UTILISATEURS_DEMO

    if query:
        utilisateurs = [
            u for u in utilisateurs
            if query.lower() in u['first_name'].lower()
            or query.lower() in u['last_name'].lower()
            or query.lower() in u['email'].lower()
            or query.lower() in u['role_label'].lower()
        ]

    return render(request, 'accounts/utilisateur_liste.html', {
        'utilisateurs': utilisateurs,
        'query': query,
        'total': len(UTILISATEURS_DEMO),
    })


def utilisateur_creer_view(request):
    """Création d'un nouveau compte utilisateur / ingénieur."""
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Le compte de {form.cleaned_data['first_name']} {form.cleaned_data['last_name']} a été créé.")
            return redirect('accounts:utilisateurs_liste')
    else:
        form = UtilisateurForm()

    return render(request, 'accounts/utilisateur_form.html', {
        'form': form,
        'titre': 'Nouveau compte utilisateur',
        'sous_titre': 'Créer un accès pour un ingénieur, chef de département ou directeur',
    })
