from django.apps import apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import FicheApplicative, HistoriqueValidation, Notification

S = FicheApplicative.Statut


def est_directeur(user):
    Directeur = apps.get_model("users", "Directeur")
    return Directeur.objects.filter(pk=user.pk).exists()


def ingenieur_pour(user):
    try:
        return user.ingenieur
    except ObjectDoesNotExist:
        pass

    Ingenieur = apps.get_model("users", "Ingenieur")
    ing = Ingenieur(user_ptr_id=user.pk)
    ing.save_base(raw=True)
    return Ingenieur.objects.get(pk=user.pk)


def _departements(fiche):
    deps = list(
        fiche.departements.select_related(
            "chef_departement", "direction__directeur"
        )
    )

    if not est_directeur(fiche.ingenieur):
        Departement = apps.get_model("organization", "Departement")
        propres = list(
            Departement.objects.select_related(
                "chef_departement", "direction__directeur"
            ).filter(chef_departement_id=fiche.ingenieur_id)
        )
        dep_ing = getattr(fiche.ingenieur, "departement", None)
        if dep_ing:
            propres.append(dep_ing)

        deja = {d.pk for d in deps}
        for d in propres:
            if d.pk not in deja:
                deps.append(d)
                deja.add(d.pk)

    return deps

def _tous_les_chefs(fiche):
    chefs = {}
    for dep in _departements(fiche):
        if dep.chef_departement_id:
            chefs[dep.chef_departement_id] = dep.chef_departement
    return chefs


def destinataires_chef(fiche):
    chefs = _tous_les_chefs(fiche)
    chefs.pop(fiche.ingenieur_id, None)
    return list(chefs.values())


def destinataires_directeur(fiche):
    directeurs = {}
    for dep in _departements(fiche):
        directeur = dep.direction.directeur
        if directeur:
            directeurs[directeur.pk] = directeur

    directeurs.pop(fiche.ingenieur_id, None)

    if not directeurs:
        Directeur = apps.get_model("users", "Directeur")
        directeurs = {
            d.pk: d for d in Directeur.objects.exclude(pk=fiche.ingenieur_id)
        }

    return list(directeurs.values())


def peut_soumettre(user, fiche):
    return (
        fiche.statut in (S.BROUILLON, S.REFUSEE)
        and fiche.ingenieur_id == user.pk
    )


def peut_valider_chef(user, fiche):
    return (
        fiche.statut == S.EN_ATTENTE
        and user.pk in {c.pk for c in destinataires_chef(fiche)}
    )


def peut_valider_directeur(user, fiche):
    return (
        fiche.statut == S.EN_VALIDATION
        and user.pk in {d.pk for d in destinataires_directeur(fiche)}
    )


def _changer_statut(fiche, auteur, nouveau, commentaire="", notifier=()):
    HistoriqueValidation.objects.create(
        fiche=fiche,
        auteur=auteur,
        ancien_statut=fiche.statut,
        nouveau_statut=nouveau,
        commentaire=commentaire,
    )

    fiche.statut = nouveau
    fiche.save(update_fields=["statut"])

    for user_id, message in notifier:
        Notification.objects.create(
            destinataire_id=user_id,
            fiche=fiche,
            message=message,
        )


def _retour(pk):
    return redirect("application_sheet:detail", pk=pk)


@require_POST
def fiche_soumettre(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if not peut_soumettre(request.user, fiche):
        messages.error(request, "Vous ne pouvez pas soumettre cette fiche.")
        return _retour(pk)

    chefs = destinataires_chef(fiche)
    auteur_est_chef = fiche.ingenieur_id in _tous_les_chefs(fiche)

    with transaction.atomic():
        if chefs:
            _changer_statut(
                fiche, request.user, S.EN_ATTENTE,
                notifier=[
                    (c.pk, f"Nouvelle fiche à valider : {fiche.nom_application} "
                            f"(de {fiche.ingenieur})")
                    for c in chefs
                ],
            )
            messages.success(request, "Fiche envoyée au chef de département.")

        elif auteur_est_chef:
            directeurs = destinataires_directeur(fiche)
            if not directeurs:
                messages.error(request, "Aucun directeur n'est défini.")
                return _retour(pk)
            _changer_statut(
                fiche, request.user, S.EN_VALIDATION,
                notifier=[
                    (d.pk, f"Fiche à confirmer : {fiche.nom_application} "
                            f"(de {fiche.ingenieur})")
                    for d in directeurs
                ],
            )
            messages.success(request, "Fiche envoyée au directeur.")

        else:
            messages.error(
                request,
                "Aucun chef de département n'est défini pour cette fiche."
            )

    return _retour(pk)


@require_POST
def fiche_valider_chef(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if not peut_valider_chef(request.user, fiche):
        messages.error(request, "Vous ne pouvez pas valider cette fiche.")
        return _retour(pk)

    directeurs = destinataires_directeur(fiche)
    if not directeurs:
        messages.error(request, "Aucun directeur n'est défini.")
        return _retour(pk)

    with transaction.atomic():
        _changer_statut(
            fiche, request.user, S.EN_VALIDATION,
            request.POST.get("commentaire", "").strip(),
            notifier=[
                (d.pk, f"Fiche validée par le chef de département, "
                        f"à confirmer : {fiche.nom_application}")
                for d in directeurs
            ] + [
                (fiche.ingenieur_id,
                    f"Votre fiche {fiche.nom_application} a été validée par "
                    f"le chef de département et envoyée au directeur.")
            ],
        )

    messages.success(request, "Fiche transmise au directeur.")
    return _retour(pk)


@require_POST
def fiche_valider_directeur(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if not peut_valider_directeur(request.user, fiche):
        messages.error(request, "Vous ne pouvez pas valider cette fiche.")
        return _retour(pk)

    with transaction.atomic():
        _changer_statut(
            fiche, request.user, S.VALIDEE,
            request.POST.get("commentaire", "").strip(),
            notifier=[
                (fiche.ingenieur_id,
                    f"Votre fiche {fiche.nom_application} a été validée "
                    f"par le directeur."),
            ],
        )

    messages.success(request, "Fiche validée.")
    return _retour(pk)


@require_POST
def fiche_refuser(request, pk):
    fiche = get_object_or_404(FicheApplicative, pk=pk)

    if not (
        peut_valider_chef(request.user, fiche)
        or peut_valider_directeur(request.user, fiche)
    ):
        messages.error(request, "Vous ne pouvez pas refuser cette fiche.")
        return _retour(pk)

    motif = request.POST.get("commentaire", "").strip()
    if not motif:
        messages.error(request, "Un motif de refus est obligatoire.")
        return _retour(pk)

    with transaction.atomic():
        _changer_statut(
            fiche, request.user, S.REFUSEE, motif,
            notifier=[
                (fiche.ingenieur_id,
                    f"Votre fiche {fiche.nom_application} a été refusée. "
                    f"Motif : {motif}"),
            ],
        )

    messages.warning(request, "Fiche refusée.")
    return _retour(pk)

def peut_modifier(user, fiche):
    if fiche.statut not in (S.BROUILLON, S.REFUSEE):
        return False

    if fiche.ingenieur_id == user.pk:
        return True

    try:
        dep_id = user.ingenieur.departement_id
    except ObjectDoesNotExist:
        return False

    if not dep_id:
        return False

    ids = set(fiche.departements.values_list("pk", flat=True))
    dep_auteur = getattr(fiche.ingenieur, "departement_id", None)
    if dep_auteur:
        ids.add(dep_auteur)

    return dep_id in ids


def peut_supprimer(user, fiche):
    if fiche.ingenieur_id == user.pk:
        return True

    return any(
        dep.direction.directeur_id == user.pk
        for dep in _departements(fiche)
    )


def enregistrer_modification(fiche, auteur, sections):
    if not sections:
        return

    HistoriqueValidation.objects.create(
        fiche=fiche,
        auteur=auteur,
        ancien_statut=fiche.statut,
        nouveau_statut=fiche.statut,
        commentaire="Modification : " + ", ".join(sections),
    )

    if fiche.ingenieur_id != auteur.pk:
        Notification.objects.create(
            destinataire_id=fiche.ingenieur_id,
            fiche=fiche,
            message=f"Votre fiche {fiche.nom_application} a été modifiée "
                    f"par {auteur}.",
        )