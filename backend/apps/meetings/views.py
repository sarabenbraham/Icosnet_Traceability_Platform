from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.db.models import ProtectedError
from .models import Lieu, Reunion, Participation, nom_complet, StatutParticipation

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.http import url_has_allowed_host_and_scheme

from .notifications import notifier_invitation
from .permissions import est_gestionnaire, gestionnaire_required

from .forms import (
    LieuForm,
    ReunionForm,
    ParticipationForm,
)


# =========================================================
# LIEUX
# =========================================================
@gestionnaire_required
def lieu_list(request):
    lieux = Lieu.objects.all()

    return render(
        request,
        "meetings/lieu_list.html",
        {
            "lieux": lieux,
        },
    )

@gestionnaire_required
def lieu_create(request):
    if request.method == "POST":
        form = LieuForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le lieu a été créée avec succès."
            )

            return redirect("meetings:lieu_list")

    else:
        form = LieuForm()

    return render(
        request,
        "meetings/lieu_form.html",
        {
            "form": form,
        },
    )

@gestionnaire_required
def lieu_detail(request, pk):
    lieu = get_object_or_404(Lieu, pk=pk)
    return render(request, "meetings/lieu_detail.html", {
        "lieu": lieu,
        "reunions": lieu.reunions.order_by("-date", "-heure_debut"),  # manquait
    })

@gestionnaire_required
def lieu_update(request, pk):
    lieu = get_object_or_404(Lieu, pk=pk)

    if request.method == "POST":
        form = LieuForm(
            request.POST,
            instance=lieu,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le lieu a été modifiée avec succès."
            )

            return redirect(
                "meetings:lieu_detail",
                pk=lieu.pk,
            )

    else:
        form = LieuForm(instance=lieu)

    return render(
        request,
        "meetings/lieu_form.html",
        {
            "form": form,
            "lieu": lieu,
        },
    )

@gestionnaire_required
def lieu_delete(request, pk):
    lieu = get_object_or_404(Lieu, pk=pk)
    if request.method == "POST":
        try:
            lieu.delete()
            messages.success(request, "Le lieu a été supprimé avec succès.")
            return redirect("meetings:lieu_list")
        except ProtectedError:
            messages.error(request, "Ce lieu est utilisé par des réunions : suppression impossible.")
            return redirect("meetings:lieu_detail", pk=lieu.pk)
    return render(request, "meetings/lieu_confirm_delete.html", {"lieu": lieu})


# =========================================================
# REUNIONS
# =========================================================
@login_required
def reunion_list(request):
    reunions = Reunion.objects.select_related("lieu").all()

    query = request.GET.get("q", "").strip()
    filtre_type = request.GET.get("type", "").strip()
    filtre_statut = request.GET.get("statut", "").strip()

    if query:
        reunions = reunions.filter(
            models.Q(objet__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(organisateur__icontains=query)
        )

    if filtre_type:
        reunions = reunions.filter(type=filtre_type)

    if filtre_statut:
        reunions = reunions.filter(statut=filtre_statut)

    if not est_gestionnaire(request.user):
        reunions = reunions.filter(
            pk__in=Participation.objects.filter(utilisateur=request.user).values("reunion")
        )


    return render(
        request,
        "meetings/reunion_list.html",
        {
            "reunions": reunions,
            "query": query,
            "filtre_type": filtre_type,
            "filtre_statut": filtre_statut,
        },
    )

@gestionnaire_required
def reunion_create(request):
    if request.method == "POST":
        form = ReunionForm(request.POST)

        if form.is_valid():
            reunion = form.save()

            messages.success(
                request,
                "La réunion a été créée avec succès."
            )

            return redirect(
                "meetings:reunion_detail",
                pk=reunion.pk,
            )

    else:
        form = ReunionForm()

    return render(
        request,
        "meetings/reunion_form.html",
        {
            "form": form,
        },
    )

@login_required
def reunion_detail(request, pk):
    reunion = get_object_or_404(
        Reunion.objects.select_related(
            "lieu",
        ),
        pk=pk,
    )

    if not est_gestionnaire(request.user) and not reunion.participations.filter(
        utilisateur=request.user
    ).exists():
        raise PermissionDenied

    participations = reunion.participations.select_related("utilisateur")


    return render(
        request,
        "meetings/reunion_detail.html",
        {
            "reunion": reunion,
            "participations": participations,
        },
    )

@gestionnaire_required
def reunion_update(request, pk):
    reunion = get_object_or_404(
        Reunion,
        pk=pk,
    )

    if request.method == "POST":
        form = ReunionForm(
            request.POST,
            instance=reunion,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La réunion a été modifiée avec succès."
            )

            return redirect(
                "meetings:reunion_detail",
                pk=reunion.pk,
            )

    else:
        form = ReunionForm(
            instance=reunion,
        )

    return render(
        request,
        "meetings/reunion_form.html",
        {
            "form": form,
            "reunion": reunion,
        },
    )

@gestionnaire_required
def reunion_delete(request, pk):
    reunion = get_object_or_404(
        Reunion,
        pk=pk,
    )

    if request.method == "POST":
        reunion.delete()

        messages.success(
            request,
            "La réunion a été supprimée avec succès."
        )

        return redirect(
            "meetings:reunion_list"
        )

    return render(
        request,
        "meetings/reunion_confirm_delete.html",
        {
            "reunion": reunion,
        },
    )


# =========================================================
# PARTICIPATIONS
# =========================================================
@gestionnaire_required
def participation_create(request, reunion_pk):
    reunion = get_object_or_404(Reunion.objects.select_related("lieu"), pk=reunion_pk)

    if request.method == "POST":
        form = ParticipationForm(request.POST, reunion=reunion)
        if form.is_valid():
            utilisateurs = list(form.cleaned_data["participants"])
            externes = list(dict.fromkeys(
                l.strip() for l in form.cleaned_data["externes"].splitlines() if l.strip()
            ))

            deja_utilisateurs = set(
                reunion.participations.filter(utilisateur__isnull=False)
                .values_list("utilisateur_id", flat=True)
            )
            deja_externes = set(
                reunion.participations.filter(utilisateur__isnull=True)
                .values_list("participant", flat=True)
            )
            utilisateurs = [u for u in utilisateurs if u.pk not in deja_utilisateurs]
            externes = [n for n in externes if n not in deja_externes]
            total = len(utilisateurs) + len(externes)

            lieu = reunion.lieu
            if total == 0:
                form.add_error(None, "Aucun nouveau participant sélectionné.")
            elif (
                lieu
                and not lieu.places_illimitees
                and lieu.capacite is not None
                and reunion.nb_participants + total > lieu.capacite
            ):
                restantes = max(lieu.capacite - reunion.nb_participants, 0)
                form.add_error(None, f"Capacité dépassée : il reste {restantes} place(s).")
            else:
                role = form.cleaned_data["role"]
                for u in utilisateurs:
                    p = Participation.objects.create(
                        reunion=reunion,
                        utilisateur=u,
                        participant=nom_complet(u),
                        role=role,
                    )
                    notifier_invitation(request, p)
                for nom in externes:
                    Participation.objects.create(
                        reunion=reunion,
                        participant=nom,
                        role=role,
                    )
                messages.success(request, f"{total} participant(s) ajouté(s).")
                return redirect("meetings:reunion_detail", pk=reunion.pk)
    else:
        form = ParticipationForm(reunion=reunion)

    return render(
        request,
        "meetings/participation_form.html",
        {"form": form, "reunion": reunion},
    )

@gestionnaire_required
def participation_delete(request, pk):
    participation = get_object_or_404(
        Participation,
        pk=pk,
    )

    reunion_pk = participation.reunion.pk

    if request.method == "POST":
        participation.delete()

        messages.success(
            request,
            "La participation a été supprimée."
        )

        return redirect(
            "meetings:reunion_detail",
            pk=reunion_pk,
        )

    return render(
        request,
        "meetings/participation_confirm_delete.html",
        {
            "participation": participation,
        },
    )

def _repondre(request, pk, action, message):
    participation = get_object_or_404(
        Participation.objects.select_related("reunion", "utilisateur"), pk=pk
    )
    # Seul l'invité lui-même ou un gestionnaire (pour les externes) peut répondre
    if not (
        est_gestionnaire(request.user)
        or participation.utilisateur_id == request.user.pk
    ):
        raise PermissionDenied

    if request.method == "POST":
        getattr(participation, action)()
        messages.success(request, message)

    suivant = request.POST.get("next", "")
    if suivant and url_has_allowed_host_and_scheme(suivant, allowed_hosts={request.get_host()}):
        return redirect(suivant)
    return redirect("meetings:reunion_detail", pk=participation.reunion.pk)


@login_required
def participation_confirmer(request, pk):
    return _repondre(request, pk, "confirmer", "La participation a été confirmée.")


@login_required
def participation_refuser(request, pk):
    return _repondre(request, pk, "refuser", "La participation a été refusée.")

@login_required
def mes_invitations(request):
    participations = (
        Participation.objects.filter(utilisateur=request.user)
        .select_related("reunion", "reunion__lieu")
        .order_by("reunion__date", "reunion__heure_debut")
    )
    return render(request, "meetings/mes_invitations.html", {"participations": participations})
