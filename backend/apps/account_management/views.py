from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Compte
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CompteForm, LoginForm, UtilisateurCompteForm


def compte_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    next_url = request.POST.get("next") or request.GET.get("next", "")
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        if url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect("dashboard")

    return render(
        request,
        "account_management/login.html",
        {"form": form, "next": next_url},
    )


def compte_logout(request):
    logout(request)
    return render(request, "account_management/logout.html")


def compte_list(request):
    from django.db.models import Q

    comptes = Compte.objects.select_related("utilisateur").filter(archive=False)

    # --- Recherche & Filtres ---
    q         = request.GET.get("q", "").strip()
    statut    = request.GET.get("statut", "").strip()
    poste     = request.GET.get("poste", "").strip()

    if q:
        comptes = comptes.filter(
            Q(utilisateur__first_name__icontains=q) |
            Q(utilisateur__last_name__icontains=q)  |
            Q(utilisateur__username__icontains=q)   |
            Q(email_connexion__icontains=q)
        )

    if statut in ("ACTIF", "DESACTIVE"):
        comptes = comptes.filter(statut=statut)

    if poste:
        comptes = comptes.filter(utilisateur__poste__iexact=poste)

    # Postes distincts pour le filtre
    postes_dispo = (
        Compte.objects.select_related("utilisateur")
        .filter(archive=False)
        .exclude(utilisateur__poste__isnull=True)
        .exclude(utilisateur__poste="")
        .values_list("utilisateur__poste", flat=True)
        .distinct()
        .order_by("utilisateur__poste")
    )

    return render(
        request,
        "account_management/utilisateur_liste.html",
        {
            "utilisateurs": [compte.utilisateur for compte in comptes],
            "total": comptes.count(),
            "titre": "Comptes utilisateurs",
            "sous_titre": "Gestion des comptes d'accès",
            # filtres
            "q": q,
            "filtre_statut": statut,
            "filtre_poste": poste,
            "postes_dispo": postes_dispo,
        },
)


def compte_detail(request, pk):
    compte = get_object_or_404(
        Compte.objects.select_related("utilisateur"),
        pk=pk,
    )

    return render(
        request,
        "account_management/utilisateur_detail.html",
        {
            "compte": compte,
            "titre": "Détail du compte",
            "sous_titre": "Informations du compte",
        },
    )



def compte_update(request, pk):
    compte = get_object_or_404(Compte, pk=pk)

    if request.method == "POST":
        form = CompteForm(request.POST, instance=compte)

        if form.is_valid():
            form.save()
            messages.success(request, "Le compte a été modifié avec succès.")
            return redirect(
                "account_management:detail",
                pk=compte.pk,
            )

    else:
        form = CompteForm(instance=compte)

    return render(
        request,
        "account_management/utilisateur_update.html",
        {
            "form": form,
            "compte": compte,
            "titre": "Modifier le compte",
            "sous_titre": "Modifier les informations du compte",
            "mode": "modifier",
        },
    )


def compte_archiver(request, pk):
    compte = get_object_or_404(Compte, pk=pk)

    if request.method == "POST":
        from django.utils import timezone as tz
        compte.archive = True
        compte.date_archivage = tz.now()
        compte.statut = Compte.Statut.DESACTIVE
        compte.save(update_fields=["archive", "date_archivage", "statut"])
        messages.success(request, "Le compte a été archivé avec succès.")
        return redirect("account_management:liste")

    return render(
        request,
        "account_management/utilisateur_archiver.html",
        {
            "compte": compte,
            "titre": "Archiver le compte",
            "sous_titre": "Confirmation d'archivage",
        },
    )


def comptes_archives(request):
    comptes = Compte.objects.select_related("utilisateur").filter(archive=True)
    return render(
        request,
        "account_management/utilisateur_archives.html",
        {
            "comptes": comptes,
            "total": comptes.count(),
            "titre": "Comptes archivés",
            "sous_titre": "Historique des comptes désactivés",
        },
    )

def compte_create(request):
    if request.method == "POST":
        form = UtilisateurCompteForm(request.POST)

        if form.is_valid():
            utilisateur = form.save()

            messages.success(
                request,
                "L'utilisateur et son compte ont été créés avec succès."
            )

            return redirect(
                "account_management:detail",
                pk=utilisateur.compte.pk,
            )

    else:
        form = UtilisateurCompteForm()

    return render(
        request,
        "account_management/utilisateur_form.html",
        {
            "form": form,
            "titre": "Créer un utilisateur",
            "sous_titre": "Créer un utilisateur et son compte",
        },
    )

@login_required
def mon_profil(request):
    compte = get_object_or_404(
        Compte.objects.select_related("utilisateur"),
        utilisateur=request.user,
    )
    return render(
        request,
        "account_management/profil.html",
        {
            "compte": compte,
            "titre": "Mon profil",
            "sous_titre": "Informations de mon compte",
        },
    )

def compte_autocomplete(request):
    """Retourne des suggestions JSON pour l'autocomplétion de la recherche."""
    from django.db.models import Q, Value
    from django.db.models.functions import Concat
    import json

    q = request.GET.get("q", "").strip()
    results = []

    if len(q) >= 2:
        comptes = (
            Compte.objects
            .select_related("utilisateur")
            .filter(archive=False)
            .filter(
                Q(utilisateur__first_name__icontains=q) |
                Q(utilisateur__last_name__icontains=q)  |
                Q(utilisateur__username__icontains=q)   |
                Q(email_connexion__icontains=q)
            )[:8]  # max 8 suggestions
        )

        for c in comptes:
            u = c.utilisateur
            full_name = u.get_full_name() or u.username
            results.append({
                "label": full_name,
                "sub": f"@{u.username} · {c.email_connexion}",
                "initial": (u.first_name[:1] or u.username[:1]).upper(),
                "value": full_name,
                "url": f"/account_management/{c.pk}/detail/",
            })

    return JsonResponse({"results": results})
