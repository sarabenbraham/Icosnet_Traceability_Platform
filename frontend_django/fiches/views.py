import json
import urllib.request
import urllib.error
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FicheApplicativeForm

# URL du backend API REST de Sara
BACKEND_API_URL = "http://127.0.0.1:8000/api/fiches/"

# Données de démonstration (fallback)
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
        'description': 'Système ERP principal pour la gestion commerciale et financière d\'ICOSNET.',
        'ingenieur': 'Ahmed Benali',
        'date_creation': '01/07/2026',
        'infrastructure': {
            'type_infrastructure': 'On-Premise',
            'plateforme_virtualisation': 'Proxmox VE',
            'ip_lan': '192.168.10.50',
            'ip_publique': '197.112.20.10',
            'systeme': 'Debian Linux',
            'version_os': '12 (Bookworm)',
            'cpu': '16 vCPU',
            'ram': '32 Go',
            'type_sgbd': 'PostgreSQL',
            'version_sgbd': '15.2',
        },
        'contrat': {
            'fournisseur': 'SAGE France',
            'reference_contrat': 'CTR-SAGE-2026',
            'budget_annuel': '2 500 000.00',
            'support_externe': True,
        },
        'developpement': {
            'mode_developpement': 'Éditeur Externe',
            'gestion_sources': 'https://gitlab.icosnet.com/dsi/sage-connect',
            'processus_ci_cd': 'GitLab CI / Deployment Playbooks',
        },
        'interventions': [
            {'date_heure': '05/08/2026 14:30', 'intervenant': 'Ahmed Benali', 'type_intervention': 'Mise à jour mineure', 'statut': 'SUCCES'},
            {'date_heure': '20/07/2026 10:00', 'intervenant': 'Karim Messaoud', 'type_intervention': 'Migration BDD', 'statut': 'SUCCES'}
        ]
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
        'description': 'Plateforme VoIP et gestion de téléphonie IP pour les abonnés et collaborateurs.',
        'ingenieur': 'Karim Messaoud',
        'date_creation': '15/07/2026',
        'infrastructure': {
            'type_infrastructure': 'On-Premise',
            'plateforme_virtualisation': 'Docker / Kubernetes',
            'ip_lan': '192.168.20.15',
            'ip_publique': '197.112.20.15',
            'systeme': 'Ubuntu Server',
            'version_os': '22.04 LTS',
            'cpu': '8 vCPU',
            'ram': '16 Go',
            'type_sgbd': 'MySQL / MariaDB',
            'version_sgbd': '10.11',
        },
        'contrat': {
            'fournisseur': 'Asterisk / Solution Telco',
            'reference_contrat': 'CTR-TELCO-2025',
            'budget_annuel': '800 000.00',
            'support_externe': False,
        },
        'developpement': {
            'mode_developpement': 'Développé en interne',
            'gestion_sources': 'https://gitlab.icosnet.com/telco/pabx-core',
            'processus_ci_cd': 'Docker Pipeline CI',
        }
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
        'description': 'Annuaire centralisé LDAP/AD pour la gestion de l\'authentification et des rôles.',
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
        'description': 'Plateforme d\'analyse décisionnelle et génération de rapports mensuels DSI.',
        'ingenieur': 'Farah Laggoune',
        'date_creation': '28/07/2026',
    },
]


def fetch_api_fiches():
    """Tente de récupérer les fiches depuis l'API REST de Sara, sinon retourne les données démo."""
    try:
        req = urllib.request.Request(BACKEND_API_URL, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if isinstance(data, list) and len(data) > 0:
                    return data
    except Exception:
        pass
    return FICHES_DEMO


def fiche_liste(request):
    """Liste de toutes les fiches applicatives avec recherche et filtre."""
    fiches = fetch_api_fiches()
    query = request.GET.get('q', '')
    filtre_statut = request.GET.get('statut', '')
    filtre_domaine = request.GET.get('domaine', '')

    if query:
        fiches = [f for f in fiches if query.lower() in f.get('nom_application', '').lower()
                  or query.lower() in f.get('code_application', '').lower()]
    if filtre_statut:
        fiches = [f for f in fiches if f.get('statut') == filtre_statut]
    if filtre_domaine:
        fiches = [f for f in fiches if f.get('domaine_fonctionnel') == filtre_domaine]

    contexte = {
        'fiches': fiches,
        'query': query,
        'filtre_statut': filtre_statut,
        'filtre_domaine': filtre_domaine,
        'total': len(fiches),
    }
    return render(request, 'fiches/fiche_liste.html', contexte)


def fiche_detail(request, pk):
    """Détail complet d'une fiche applicative."""
    fiches = fetch_api_fiches()
    fiche = next((f for f in fiches if f.get('id') == pk or str(f.get('id')) == str(pk)), None)

    if fiche is None:
        messages.error(request, "Fiche introuvable.")
        return redirect('fiches:liste')
    return render(request, 'fiches/fiche_detail.html', {'fiche': fiche})


def fiche_creer(request):
    """Formulaire de création d'une nouvelle fiche applicative."""
    if request.method == 'POST':
        form = FicheApplicativeForm(request.POST)
        if form.is_valid():
            messages.success(request, f"La fiche « {form.cleaned_data['nom_application']} » a été enregistrée.")
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
    fiches = fetch_api_fiches()
    fiche = next((f for f in fiches if f.get('id') == pk or str(f.get('id')) == str(pk)), None)

    if fiche is None:
        messages.error(request, "Fiche introuvable.")
        return redirect('fiches:liste')

    if request.method == 'POST':
        form = FicheApplicativeForm(request.POST)
        if form.is_valid():
            messages.success(request, f"La fiche « {form.cleaned_data['nom_application']} » a été mise à jour.")
            return redirect('fiches:detail', pk=pk)
    else:
        form = FicheApplicativeForm(initial=fiche)

    return render(request, 'fiches/fiche_form.html', {
        'form': form,
        'fiche': fiche,
        'titre': f'Modifier — {fiche.get("nom_application")}',
        'sous_titre': 'Mise à jour des informations de la fiche applicative',
        'mode': 'modifier',
    })
