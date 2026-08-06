from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from .forms import (
    ContratForm,
    DeveloppementForm,
    FicheApplicativeForm,
    FluxApplicationForm,
    InfrastructureForm,
    IntegrationForm,
    InterventionForm,
    ModuleMetierForm,
    SauvegardeForm,
    StockageForm,
    UtilisateurAccesForm,
)

from .models import (
    Contrat,
    Developpement,
    FicheApplicative,
    FluxApplication,
    Infrastructure,
    Integration,
    Intervention,
    ModuleMetier,
    Sauvegarde,
    Stockage,
    UtilisateurAcces,
)


# ── Formsets pour les relations 1-N ──
FluxFormSet = inlineformset_factory(
    FicheApplicative,
    FluxApplication,
    form=FluxApplicationForm,
    extra=1,
    can_delete=True,
)

InterventionFormSet = inlineformset_factory(
    FicheApplicative,
    Intervention,
    form=InterventionForm,
    extra=1,
    can_delete=True,
)

ModuleFormSet = inlineformset_factory(
    FicheApplicative,
    ModuleMetier,
    form=ModuleMetierForm,
    extra=1,
    can_delete=True,
)


class FicheApplicativeListView(ListView):
    model = FicheApplicative
    template_name = "application_sheet/fiche_list.html"
    context_object_name = "fiches"
    ordering = ["-date_creation"]


def fiche_detail(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    return render(
        request,
        "application_sheet/fiche_detail.html",
        {
            "page_title": fiche.nom_application,
            "fiche": fiche,
        },
    )


@transaction.atomic
def fiche_create(request):

    if request.method == "POST":

        fiche_form = FicheApplicativeForm(request.POST)

        if fiche_form.is_valid():

            fiche = fiche_form.save()

            Contrat.objects.create(fiche=fiche)

            Infrastructure.objects.create(
                fiche=fiche,
                type_infrastructure="ON_PREMISE",
                plateforme_virtualisation="PHYSIQUE",
                cluster="",
                machine="",
                serveur_application="",
                ip_serveur_application="0.0.0.0",
                cpu="",
                ram="",
                ip_lan="0.0.0.0",
                systeme="",
                version_os="",
                type_sgbd="",
                version_sgbd="",
            )

            UtilisateurAcces.objects.create(fiche=fiche)

            Developpement.objects.create(
                fiche=fiche,
                mode_developpement="INTERNE",
                gestion_sources="",
                processus_ci_cd="",
                environnements=[],
                methode_personnalisation="",
                livrables_personnalisation="",
                services="",
            )

            Stockage.objects.create(fiche=fiche)

            Integration.objects.create(
                fiche=fiche,
                messagerie="",
                compte_messagerie="",
                usage="",
            )

            Sauvegarde.objects.create(
                fiche=fiche,
                emplacement_logs="",
                supervision="",
            )

            # FluxApplication et Intervention ne sont PAS créés ici :
            # ce sont des relations 1-N, gérées via formsets dans fiche_update.

            messages.success(
                request,
                "La fiche applicative a été créée.",
            )

            return redirect("application_sheet:fiche_update", pk=fiche.pk)

    else:

        fiche_form = FicheApplicativeForm()

    return render(
        request,
        "application_sheet/fiche_form.html",
        {
            "page_title": "Nouvelle fiche applicative",
            "fiche_form": fiche_form,
        },
    )


@transaction.atomic
def fiche_update(request, pk):

    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if request.method == "POST":

        fiche_form = FicheApplicativeForm(request.POST, instance=fiche)
        contrat_form = ContratForm(request.POST, instance=fiche.contrat)
        infrastructure_form = InfrastructureForm(request.POST, instance=fiche.infrastructure)
        utilisateur_form = UtilisateurAccesForm(request.POST, instance=fiche.utilisateurs_acces)
        developpement_form = DeveloppementForm(request.POST, instance=fiche.developpement)
        stockage_form = StockageForm(request.POST, instance=fiche.stockage)
        integration_form = IntegrationForm(request.POST, instance=fiche.integration)
        sauvegarde_form = SauvegardeForm(request.POST, instance=fiche.sauvegarde)

        # Relations 1-N -> formsets, pas ModelForm simple
        flux_formset = FluxFormSet(request.POST, instance=fiche, prefix="flux")
        intervention_formset = InterventionFormSet(request.POST, instance=fiche, prefix="intervention")
        module_formset = ModuleFormSet(request.POST, instance=fiche, prefix="module")

        forms_valid = (
            fiche_form.is_valid()
            and contrat_form.is_valid()
            and infrastructure_form.is_valid()
            and utilisateur_form.is_valid()
            and developpement_form.is_valid()
            and stockage_form.is_valid()
            and integration_form.is_valid()
            and sauvegarde_form.is_valid()
            and flux_formset.is_valid()
            and intervention_formset.is_valid()
            and module_formset.is_valid()
        )

        if forms_valid:

            fiche_form.save()
            contrat_form.save()
            infrastructure_form.save()
            utilisateur_form.save()
            developpement_form.save()
            stockage_form.save()
            integration_form.save()
            sauvegarde_form.save()
            flux_formset.save()
            intervention_formset.save()
            module_formset.save()

            messages.success(
                request,
                "La fiche applicative a été mise à jour.",
            )

            return redirect("application_sheet:fiche_update", pk=fiche.pk)

    else:

        fiche_form = FicheApplicativeForm(instance=fiche)
        contrat_form = ContratForm(instance=fiche.contrat)
        infrastructure_form = InfrastructureForm(instance=fiche.infrastructure)
        utilisateur_form = UtilisateurAccesForm(instance=fiche.utilisateurs_acces)
        developpement_form = DeveloppementForm(instance=fiche.developpement)
        stockage_form = StockageForm(instance=fiche.stockage)
        integration_form = IntegrationForm(instance=fiche.integration)
        sauvegarde_form = SauvegardeForm(instance=fiche.sauvegarde)

        flux_formset = FluxFormSet(instance=fiche, prefix="flux")
        intervention_formset = InterventionFormSet(instance=fiche, prefix="intervention")
        module_formset = ModuleFormSet(instance=fiche, prefix="module")

    return render(
        request,
        "application_sheet/fiche_form.html",
        {
            "page_title": "Modifier la fiche applicative",
            "fiche": fiche,
            "fiche_form": fiche_form,
            "contrat_form": contrat_form,
            "infrastructure_form": infrastructure_form,
            "utilisateur_form": utilisateur_form,
            "developpement_form": developpement_form,
            "stockage_form": stockage_form,
            "integration_form": integration_form,
            "sauvegarde_form": sauvegarde_form,
            "flux_formset": flux_formset,
            "intervention_formset": intervention_formset,
            "module_formset": module_formset,
        },
    )


class FicheApplicativeDeleteView(DeleteView):
    model = FicheApplicative
    template_name = "application_sheet/fiche_confirm_delete.html"
    success_url = reverse_lazy("application_sheet:fiche_list")

