from django.contrib import messages
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
    comptes = Compte.objects.select_related("utilisateur").all()

    return render(
        request,
        "account_management/utilisateur_liste.html",
        {
            "utilisateurs": [compte.utilisateur for compte in comptes],
            "total": comptes.count(),
            "titre": "Comptes utilisateurs",
            "sous_titre": "Gestion des comptes d'accès",
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


def compte_delete(request, pk):
    compte = get_object_or_404(Compte, pk=pk)

    if request.method == "POST":
        compte.delete()
        messages.success(request, "Le compte a été supprimé avec succès.")
        return redirect("account_management:liste")

    return render(
        request,
        "account_management/utilisateur_delete.html",
        {
            "compte": compte,
            "titre": "Supprimer le compte",
            "sous_titre": "Confirmation de suppression",
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