from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CompteForm, UtilisateurCompteForm
from .models import Compte


def compte_list(request):
    comptes = Compte.objects.select_related("utilisateur").all()

    return render(
        request,
        "account_management/compte_list.html",
        {
            "comptes": comptes,
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
        "account_management/compte_detail.html",
        {
            "compte": compte,
            "titre": "Détail du compte",
            "sous_titre": "Informations du compte",
        },
    )


def compte_create(request):
    if request.method == "POST":
        form = CompteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le compte a été créé avec succès.")
            return redirect("account_management:liste")

    else:
        form = CompteForm()

    return render(
        request,
        "account_management/compte_form.html",
        {
            "form": form,
            "titre": "Créer un compte",
            "sous_titre": "Ajouter un compte utilisateur",
            "mode": "creer",
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
        "account_management/compte_form.html",
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
        "account_management/compte_confirm_delete.html",
        {
            "compte": compte,
            "titre": "Supprimer le compte",
            "sous_titre": "Confirmation de suppression",
        },
    )

def utilisateur_compte_create(request):
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
        "account_management/utilisateur_compte_form.html",
        {
            "form": form,
            "titre": "Créer un utilisateur",
            "sous_titre": "Créer un utilisateur et son compte",
        },
    )