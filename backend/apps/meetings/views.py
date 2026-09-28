from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    LieuForm,
    ReunionForm,
    ParticipationForm,
)
from .models import (
    Lieu,
    Reunion,
    Participation,
)


# =========================================================
# LIEUX
# =========================================================

def lieu_list(request):
    lieux = Lieu.objects.all()

    return render(
        request,
        "meetings/lieu_list.html",
        {
            "lieux": lieux,
        },
    )


def lieu_create(request):
    if request.method == "POST":
        form = LieuForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La salle a été créée avec succès."
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


def lieu_detail(request, pk):
    lieu = get_object_or_404(Lieu, pk=pk)

    return render(
        request,
        "meetings/lieu_detail.html",
        {
            "lieu": lieu,
        },
    )


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
                "La salle a été modifiée avec succès."
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


def lieu_delete(request, pk):
    lieu = get_object_or_404(Lieu, pk=pk)

    if request.method == "POST":
        lieu.delete()

        messages.success(
            request,
            "La salle a été supprimée avec succès."
        )

        return redirect("meetings:lieu_list")

    return render(
        request,
        "meetings/lieu_confirm_delete.html",
        {
            "lieu": lieu,
        },
    )


# =========================================================
# REUNIONS
# =========================================================

def reunion_list(request):
    reunions = Reunion.objects.select_related(
        "lieu",
    ).all()

    return render(
        request,
        "meetings/reunion_list.html",
        {
            "reunions": reunions,
        },
    )


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


def reunion_detail(request, pk):
    reunion = get_object_or_404(
        Reunion.objects.select_related(
            "lieu",
        ),
        pk=pk,
    )

    participations = reunion.participations.all()

    return render(
        request,
        "meetings/reunion_detail.html",
        {
            "reunion": reunion,
            "participations": participations,
        },
    )


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

def participation_create(request, reunion_pk):
    reunion = get_object_or_404(
        Reunion,
        pk=reunion_pk,
    )

    if request.method == "POST":
        form = ParticipationForm(request.POST)

        if form.is_valid():
            participation = form.save(commit=False)
            participation.reunion = reunion

            participation.full_clean()
            participation.save()

            messages.success(
                request,
                "Le participant a été ajouté à la réunion."
            )

            return redirect(
                "meetings:reunion_detail",
                pk=reunion.pk,
            )

    else:
        form = ParticipationForm()

    return render(
        request,
        "meetings/participation_form.html",
        {
            "form": form,
            "reunion": reunion,
        },
    )


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


def participation_confirmer(request, pk):
    participation = get_object_or_404(
        Participation,
        pk=pk,
    )

    if request.method == "POST":
        participation.confirmer()

        messages.success(
            request,
            "La participation a été confirmée."
        )

    return redirect(
        "meetings:reunion_detail",
        pk=participation.reunion.pk,
    )


def participation_refuser(request, pk):
    participation = get_object_or_404(
        Participation,
        pk=pk,
    )

    if request.method == "POST":
        participation.refuser()

        messages.success(
            request,
            "La participation a été refusée."
        )

    return redirect(
        "meetings:reunion_detail",
        pk=participation.reunion.pk,
    )