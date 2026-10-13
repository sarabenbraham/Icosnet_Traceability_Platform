from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from apps.application_sheet.models import FicheApplicative
from apps.meetings.models import Reunion
from apps.meetings.permissions import roles_utilisateur
from apps.organization.models import Departement

Statut = FicheApplicative.Statut


@login_required
def home(request):
    user = request.user
    roles = roles_utilisateur(user)

    is_directeur = "directeur" in roles
    is_chef = "chefdepartement" in roles
    is_ingenieur = "ingenieur" in roles

    # ============================================================
    # 1. FICHES VISIBLES SELON LE RÔLE
    # ============================================================

    toutes_les_fiches = (
        FicheApplicative.objects
        .select_related("ingenieur")
        .prefetch_related("departements")
        .order_by("-date_creation")
    )

    if is_directeur:
        # Le directeur voit toutes les fiches
        fiches = toutes_les_fiches

    elif is_chef:
        # Le chef voit les fiches de son département :
        # celles rattachées à ce département ET celles de ses ingénieurs
        # (même règle que dans workflow.py)
        departement = (
            Departement.objects
            .filter(chef_departement__pk=user.pk)
            .first()
        )

        if departement:
            fiches = toutes_les_fiches.filter(
                Q(departements=departement)
                | Q(ingenieur__departement=departement)
            ).distinct()
        else:
            fiches = toutes_les_fiches.none()

    elif is_ingenieur:
        # L'ingénieur ne voit que ses propres fiches
        fiches = toutes_les_fiches.filter(ingenieur__pk=user.pk)

    else:
        fiches = toutes_les_fiches.none()

    # ============================================================
    # 2. FICHES À TRAITER (file d'attente de la personne connectée)
    #    chef       -> EN_ATTENTE     (soumises, à valider par le chef)
    #    directeur  -> EN_VALIDATION  (déjà validées par le chef)
    # ============================================================

    if is_directeur:
        fiches_a_traiter = fiches.filter(statut=Statut.EN_VALIDATION)

    elif is_chef:
        fiches_a_traiter = fiches.filter(statut=Statut.EN_ATTENTE)

    else:
        fiches_a_traiter = fiches.none()

    # ============================================================
    # 3. STATISTIQUES
    # ============================================================

    if is_chef or is_directeur:
        # Pour un valideur : ce qui attend SA décision
        en_cours = fiches_a_traiter.count()
    else:
        # Pour un ingénieur : ses fiches en cours de validation
        en_cours = fiches.filter(
            statut__in=[Statut.EN_ATTENTE, Statut.EN_VALIDATION]
        ).count()

    stats = {
        "total": fiches.count(),
        "validees": fiches.filter(statut=Statut.VALIDEE).count(),
        "en_attente": en_cours,
        "refusees": fiches.filter(statut=Statut.REFUSEE).count(),
        "brouillons": fiches.filter(statut=Statut.BROUILLON).count(),
    }

    # ============================================================
    # 4. FICHES RÉCENTES
    # ============================================================

    fiches_recentes = fiches[:8]

    # ============================================================
    # 5. RÉPARTITION PAR DOMAINE
    # ============================================================

    correspondance = {
        "RH": "RH",
        "COMMERCIAL": "Commercial",
        "TECHNIQUE": "Technique",
        "MIDDLEWARE": "Middleware",
        "BI": "BI",
    }

    domaines_counts = {nom: 0 for nom in correspondance.values()}

    for fiche in fiches:
        domaines = fiche.domaine_fonctionnel

        if isinstance(domaines, str):
            domaines = domaines.split(",")

        for domaine in domaines:
            nom = correspondance.get(str(domaine).strip())
            if nom:
                domaines_counts[nom] += 1

    # ============================================================
    # 6. RÉUNIONS
    # ============================================================

    reunions_count = Reunion.objects.count()

    # ============================================================
    # 7. CONTEXTE
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