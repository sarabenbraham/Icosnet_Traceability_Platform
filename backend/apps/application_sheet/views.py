from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404

from .forms import FicheApplicativeCompleteForm
from .models import FicheApplicative


def fiche_list(request):
    fiches = FicheApplicative.objects.select_related(
        "ingenieur"
    ).prefetch_related(
        "departements"
    )

    return render(
        request,
        "application_sheet/fiche_list.html",
        {
            "fiches": fiches,
        },
    )


def fiche_detail(request, pk):
    fiche = get_object_or_404(
        FicheApplicative.objects.select_related(
            "ingenieur"
        ).prefetch_related(
            "departements"
        ),
        pk=pk,
    )

    return render(
        request,
        "application_sheet/fiche_detail.html",
        {
            "fiche": fiche,
        },
    )


def fiche_delete(request, pk):
    fiche = get_object_or_404(
        FicheApplicative,
        pk=pk,
    )

    if request.method == "POST":
        fiche.delete()

        messages.success(
            request,
            "La fiche applicative a été supprimée avec succès.",
        )

        return redirect("application_sheet:fiche_list")

    return render(
        request,
        "application_sheet/fiche_confirm_delete.html",
        {
            "fiche": fiche,
        },
    )



def create_fiche_applicative(request):

    if request.method == "POST":

        form = FicheApplicativeCompleteForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                fiche = form.fiche.save()

                contrat = form.contrat.save(commit=False)
                contrat.fiche = fiche
                contrat.save()

                infrastructure = form.infrastructure.save(commit=False)
                infrastructure.fiche = fiche
                infrastructure.save()

                acces = form.acces.save(commit=False)
                acces.fiche = fiche
                acces.save()

                developpement = form.developpement.save(commit=False)
                developpement.fiche = fiche
                developpement.save()

                module_metier = form.module_metier.save(commit=False)
                module_metier.fiche = fiche
                module_metier.save()

                stockage = form.stockage.save(commit=False)
                stockage.fiche = fiche
                stockage.save()

                integration = form.integration.save(commit=False)
                integration.fiche = fiche
                integration.save()

                flux = form.flux.save(commit=False)
                flux.fiche = fiche
                flux.save()

                sauvegarde = form.sauvegarde.save(commit=False)
                sauvegarde.fiche = fiche
                sauvegarde.save()

                intervention = form.intervention.save(commit=False)
                intervention.fiche = fiche
                intervention.save()

            messages.success(
                request,
                "La fiche applicative a été créée avec succès."
            )

            return redirect(
                "application_sheet:fiche_detail",
                pk=fiche.pk
            )

    else:
        form = FicheApplicativeCompleteForm()

    return render(
        request,
        "application_sheet/fiche_form.html",
        {
            "form": form,
        }
    )