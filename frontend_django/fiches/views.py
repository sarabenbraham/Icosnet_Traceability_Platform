from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FicheApplicativeForm


# ── Données de démonstration (à remplacer par des appels API ou modèles locaux) ──
FICHES_DEMO = [
    {
        'id': 1,
        'nom_application': 'ERP SAGE X3',
        'code_application': 'ERP-001',
        'domaine_fonctionnel': 'COMMERCIAL',
        'domaine_label': 'Commercial',
        'criticite': 'CRITIQUE',
        'criticite_label': 'Critique',
        'statut': 'VALIDEE',
        'description': 'Système ERP principal pour la gestion commerciale et financière.',
        'ingenieur': 'Ahmed Benali',
        'date_creation': '01/07/2026',
    },
    {
        'id': 2,
        'nom_application': 'PABX Centrex',
        'code_application': 'TEL-001',
        'domaine_fonctionnel': 'TECHNIQUE',
        'domaine_label': 'Technique / Telco',
        'criticite': 'MAJEURE',
        'criticite_label': 'Majeure',
        'statut': 'EN_ATTENTE',
        'description': 'Système de téléphonie IP pour les communications internes et externes.',
        'ingenieur': 'Karim Messaoud',
        'date_creation': '15/07/2026',
    },
    {
        'id': 3,
        'nom_application': 'Active Directory',
        'code_application': 'MID-001',
        'domaine_fonctionnel': 'MIDDLEWARE',
        'domaine_label': 'Middleware',
        'criticite': 'CRITIQUE',
        'criticite_label': 'Critique',
        'statut': 'VALIDEE',
        'description': 'Annuaire LDAP central pour la gestion des identités et des accès.',
        'ingenieur': 'Sara Benbraham',
        'date_creation': '10/06/2026',
    },
    {
        'id': 4,
        'nom_application': 'BI Reporting Suite',
        'code_application': 'BI-001',
        'domaine_fonctionnel': 'BI',
        'domaine_label': 'Décisionnel',
        'criticite': 'MINEURE',
        'criticite_label': 'Mineure',
        'statut': 'BROUILLON',
        'description': 'Plateforme de reporting et tableaux de bord décisionnels.',
        'ingenieur': 'Farah Laggoune',
        'date_creation': '28/07/2026',
    },
]


def fiche_liste(request):
    """Liste de toutes les fiches applicatives avec recherche et filtre."""
    fiches = FICHES_DEMO
    query = request.GET.get('q', '')
    filtre_statut = request.GET.get('statut', '')
    filtre_domaine = request.GET.get('domaine', '')

    if query:
        fiches = [f for f in fiches if query.lower() in f['nom_application'].lower()
                  or query.lower() in f['code_application'].lower()]
    if filtre_statut:
        fiches = [f for f in fiches if f['statut'] == filtre_statut]
    if filtre_domaine:
        fiches = [f for f in fiches if f['domaine_fonctionnel'] == filtre_domaine]

    contexte = {
        'fiches': fiches,
        'query': query,
        'filtre_statut': filtre_statut,
        'filtre_domaine': filtre_domaine,
        'total': len(FICHES_DEMO),
    }
    return render(request, 'fiches/fiche_liste.html', contexte)


def fiche_detail(request, pk):
    """Détail complet d'une fiche applicative."""
    fiche = next((f for f in FICHES_DEMO if f['id'] == pk), None)
    if fiche is None:
        messages.error(request, "Fiche introuvable.")
        return redirect('fiches:liste')
    return render(request, 'fiches/fiche_detail.html', {'fiche': fiche})


def fiche_creer(request):
    """Formulaire de création d'une nouvelle fiche applicative."""
    if request.method == 'POST':
        form = FicheApplicativeForm(request.POST)
        if form.is_valid():
            messages.success(request, f"La fiche « {form.cleaned_data['nom_application']} » a été créée avec succès.")
            return redirect('fiches:liste')
    else:
        form = FicheApplicativeForm()

    return render(request, 'fiches/fiche_form.html', {
        'form': form,
        'titre': 'Nouvelle fiche applicative',
        'sous_titre': 'Remplissez les informations de base de l\'application',
        'mode': 'creer',
    })


def fiche_modifier(request, pk):
    """Formulaire de modification d'une fiche applicative existante."""
    fiche = next((f for f in FICHES_DEMO if f['id'] == pk), None)
    if fiche is None:
        messages.error(request, "Fiche introuvable.")
        return redirect('fiches:liste')

    if request.method == 'POST':
        form = FicheApplicativeForm(request.POST)
        if form.is_valid():
            messages.success(request, f"La fiche « {form.cleaned_data['nom_application']} » a été modifiée.")
            return redirect('fiches:detail', pk=pk)
    else:
        form = FicheApplicativeForm(initial=fiche)

    return render(request, 'fiches/fiche_form.html', {
        'form': form,
        'fiche': fiche,
        'titre': f'Modifier — {fiche["nom_application"]}',
        'sous_titre': 'Mise à jour des informations de la fiche applicative',
        'mode': 'modifier',
    })
