from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import FicheApplicativeCompleteForm
from .models import FicheApplicative, Notification
from .workflow import ingenieur_pour, peut_modifier, peut_soumettre, peut_valider_chef, peut_valider_directeur, est_directeur, peut_supprimer, enregistrer_modification

def fiche_list(request):
    fiches = FicheApplicative.objects.select_related(
        "ingenieur"
    ).prefetch_related(
        "departements"
    )

    statut = request.GET.get("statut")
    if statut:
        fiches = fiches.filter(statut=statut)

    domaine = request.GET.get("domaine")
    if domaine:
        fiches = fiches.filter(domaine_fonctionnel__contains=domaine)

    fiches = list(fiches)
    directeur = est_directeur(request.user)
    for f in fiches:
        f.peut_supprimer = peut_supprimer(request.user, f)

    return render(
        request,
        "application_sheet/fiche_liste.html",
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

    Notification.objects.filter(
        destinataire=request.user,
        fiche=fiche,
        lue=False,
    ).update(lue=True)

    return render(
        request,
        "application_sheet/fiche_detail.html",
        {
            "fiche": fiche,
            "peut_soumettre": peut_soumettre(request.user, fiche),
            "peut_valider_chef": peut_valider_chef(request.user, fiche),
            "peut_valider_directeur": peut_valider_directeur(request.user, fiche),
            "peut_modifier": peut_modifier(request.user, fiche),
            "peut_supprimer": peut_supprimer(request.user, fiche),
        },
    )


def fiche_delete(request, pk):
    fiche = get_object_or_404(
        FicheApplicative,
        pk=pk,
    )

    if not peut_supprimer(request.user, fiche):
        messages.error(request, "Vous ne pouvez pas supprimer cette fiche.")
        return redirect("application_sheet:detail", pk=pk)

    if request.method == "POST":
        fiche.delete()

        messages.success(
            request,
            "La fiche applicative a été supprimée avec succès.",
        )

        return redirect("application_sheet:liste")

    return render(
        request,
        "application_sheet/fiche_delete.html",
        {
            "fiche": fiche,
        },
    )



def create_fiche_applicative(request):

    ingenieur = ingenieur_pour(request.user)
    if ingenieur is None:
        messages.error(request, "Impossible de créer la fiche pour ce compte.")
        return redirect("application_sheet:liste")

    if request.method == "POST":
        form = FicheApplicativeCompleteForm(request.POST)
        valide = form.is_valid()

        # Un directeur doit choisir le(s) département(s) → ses chefs recevront la fiche
        if valide and est_directeur(request.user) \
                and not form.fiche.cleaned_data.get("departements"):
            form.fiche.add_error(
                "departements",
                "Choisissez le département dont le chef doit valider la fiche."
            )
            valide = False

        if valide:

            with transaction.atomic():

                fiche = form.fiche.save(commit=False)
                fiche.ingenieur = ingenieur
                fiche.save()
                form.fiche.save_m2m()

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

                form.flux.instance = fiche
                form.flux.save()

                sauvegarde = form.sauvegarde.save(commit=False)
                sauvegarde.fiche = fiche
                sauvegarde.save()

                form.intervention.instance = fiche
                form.intervention.save()

            messages.success(
                request,
                "La fiche applicative a été créée avec succès."
            )

            return redirect(
                "application_sheet:detail",
                pk=fiche.pk
            )

    else:
        form = FicheApplicativeCompleteForm()

    return render(
        request,
        "application_sheet/fiche_form.html",
        {
            "form": form,
            "mode": "creer",
            "titre": "Nouvelle fiche applicative",
            "sous_titre": "Création d'une nouvelle fiche pour une application de la DSI",
        }
    )


def fiche_update(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if not peut_modifier(request.user, fiche):
        messages.error(request, "Vous ne pouvez pas modifier cette fiche.")
        return redirect("application_sheet:detail", pk=pk)

    if request.method == "POST":
        form = FicheApplicativeCompleteForm(request.POST, instance=fiche)

        if form.is_valid():
            sections = [
                nom for nom, f in [
                    ("Identification", form.fiche),
                    ("Contrat", form.contrat),
                    ("Infrastructure", form.infrastructure),
                    ("Accès", form.acces),
                    ("Développement", form.developpement),
                    ("Modules métier", form.module_metier),
                    ("Stockage", form.stockage),
                    ("Intégration", form.integration),
                    ("Flux", form.flux),
                    ("Sauvegarde", form.sauvegarde),
                    ("Interventions", form.intervention),
                ] if f.has_changed()
            ]
            anciens_modules = list(
                getattr(fiche, "module_metier", None).modules
                if hasattr(fiche, "module_metier") else []
            )
            if form.module_metier.get_modules() != anciens_modules \
                    and "Modules métier" not in sections:
                sections.append("Modules métier")


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

                form.flux.instance = fiche
                form.flux.save()

                sauvegarde = form.sauvegarde.save(commit=False)
                sauvegarde.fiche = fiche
                sauvegarde.save()

                form.intervention.instance = fiche
                form.intervention.save()

                enregistrer_modification(fiche, request.user, sections)

            messages.success(
                request,
                "La fiche applicative a été modifiée avec succès."
            )

            return redirect("application_sheet:detail", pk=fiche.pk)
    else:
        form = FicheApplicativeCompleteForm(instance=fiche)

    return render(
        request,
        "application_sheet/fiche_update.html",
        {
            "form": form,
            "fiche": fiche,
            "mode": "modifier",
            "titre": f"Modifier {fiche.nom_application}",
            "sous_titre": "Mise à jour des informations de l'application",
        }
    )