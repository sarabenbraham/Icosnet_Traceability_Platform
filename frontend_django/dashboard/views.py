from django.shortcuts import render


def home(request):
    # Statistiques statiques pour l'instant (à connecter à l'API plus tard)
    stats = {
        'total': 0,
        'validees': 0,
        'en_attente': 0,
        'brouillons': 0,
        'refusees': 0,
    }

    # Données d'exemple pour la démonstration
    fiches_recentes = [
        {'nom_application': 'ERP SAGE X3', 'code_application': 'ERP-001', 'domaine': 'Commercial', 'criticite': 'Critique', 'statut': 'VALIDEE', 'date': '06/08/2026'},
        {'nom_application': 'PABX Centrex', 'code_application': 'TEL-001', 'domaine': 'Technique / Telco', 'criticite': 'Majeure', 'statut': 'EN_ATTENTE', 'date': '04/08/2026'},
        {'nom_application': 'Active Directory', 'code_application': 'MID-001', 'domaine': 'Middleware', 'criticite': 'Critique', 'statut': 'VALIDEE', 'date': '01/08/2026'},
        {'nom_application': 'BI Reporting', 'code_application': 'BI-001', 'domaine': 'Décisionnel', 'criticite': 'Mineure', 'statut': 'BROUILLON', 'date': '28/07/2026'},
    ]

    contexte = {
        'stats': stats,
        'fiches_recentes': fiches_recentes,
    }
    return render(request, 'dashboard/home.html', contexte)
