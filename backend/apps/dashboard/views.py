from collections import Counter

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from apps.application_sheet.models import FicheApplicative
from apps.organization.models import Departement
from apps.meetings.models import Reunion
from apps.meetings.permissions import roles_utilisateur


@login_required
def home(request):
    user = request.user
    roles = roles_utilisateur(user)

    is_directeur = "directeur" in roles
    is_chef = "chefdepartement" in roles
    is_ingenieur = "ingenieur" in roles

    # ============================================================
    # 1. DÉTERMINER LES FICHES VISIBLES SELON LE RÔLE
    # ============================================================

    toutes_les_fiches = (
        FicheApplicative.objects
        .select_related("ingenieur")
        .prefetch_related("departements")
        .order_by("-date_creation")
    )

    fiches = toutes_les_fiches

    # Ingénieur :
    # uniquement les fiches qu'il a créées
    if is_ingenieur and not is_chef and not is_directeur:
        try:
            fiches = toutes_les_fiches.filter(
                ingenieur=user.ingenieur
            )
        except AttributeError:
            fiches = toutes_les_fiches.none()

    # Chef de département :
    # fiches concernant son département
    elif is_chef and not is_directeur:
        departement_chef = (
            Departement.objects
            .filter(chef_departement=user)
            .first()
        )

        if departement_chef:
            fiches = toutes_les_fiches.filter(
                departements=departement_chef
            ).distinct()
        else:
            fiches = toutes_les_fiches.none()

    # Directeur :
    # accès à toutes les fiches
    elif is_directeur:
        fiches = toutes_les_fiches

    # ============================================================
    # 2. STATISTIQUES
    # ============================================================

    stats = {
        "total": fiches.count(),
        "validees": fiches.filter(
            statut=FicheApplicative.Statut.VALIDEE
        ).count(),
        "en_attente": fiches.filter(
            statut__in=[
                FicheApplicative.Statut.EN_ATTENTE,
                FicheApplicative.Statut.EN_VALIDATION,
            ]
        ).count(),
        "refusees": fiches.filter(
            statut=FicheApplicative.Statut.REFUSEE
        ).count(),
        "brouillons": fiches.filter(
            statut=FicheApplicative.Statut.BROUILLON
        ).count(),
    }

    # ============================================================
    # 3. FICHES À TRAITER
    # ============================================================

    if is_directeur:
        fiches_a_traiter = fiches.filter(
            statut=FicheApplicative.Statut.EN_VALIDATION
        )

    elif is_chef:
        fiches_a_traiter = fiches.filter(
            statut=FicheApplicative.Statut.EN_VALIDATION
        )

    else:
        fiches_a_traiter = fiches.none()

    # ============================================================
    # 4. FICHES RÉCENTES
    # ============================================================

    fiches_recentes = fiches[:8]

    # ============================================================
    # 5. RÉPARTITION PAR DOMAINE
    # ============================================================

    domaines_counts = {
        "RH": 0,
        "Commercial": 0,
        "Technique": 0,
        "Middleware": 0,
        "BI": 0,
    }

    for fiche in fiches:
        domaines = fiche.domaine_fonctionnel

        if isinstance(domaines, str):
            domaines = domaines.split(",")

        for domaine in domaines:
            domaine = domaine.strip()

            if domaine == "RH":
                domaines_counts["RH"] += 1

            elif domaine == "COMMERCIAL":
                domaines_counts["Commercial"] += 1

            elif domaine == "TECHNIQUE":
                domaines_counts["Technique"] += 1

            elif domaine == "MIDDLEWARE":
                domaines_counts["Middleware"] += 1

            elif domaine == "BI":
                domaines_counts["BI"] += 1

    # ============================================================
    # 6. RÉUNIONS
    # ============================================================

    reunions_count = Reunion.objects.count()

    # ============================================================
    # 7. CONTEXTE DU DASHBOARD
    # ============================================================

    context = {
        "stats": stats,
        "fiches": fiches,
        "fiches_recentes": fiches_recentes,
        "fiches_a_traiter": fiches_a_traiter,
        "domaines_counts": domaines_counts,

        "reunions_count": reunions_count,

        "is_directeur": is_directeur,
        "is_chef": is_chef,
        "is_ingenieur": is_ingenieur,

        "role": (
            "Directeur / DSI"
            if is_directeur
            else "Chef de département"
            if is_chef
            else "Ingénieur"
            if is_ingenieur
            else "Utilisateur"
        ),
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )