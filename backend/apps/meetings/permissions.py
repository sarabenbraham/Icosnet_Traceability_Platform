from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from .models import StatutParticipation, StatutReunion


from .models import StatutParticipation, StatutReunion


def est_participant_actif(user, reunion):
    """Invité n'ayant pas refusé."""
    return reunion.participations.filter(utilisateur=user).exclude(
        statut=StatutParticipation.REFUSEE
    ).exists()


def peut_editer_pv(user, reunion, pv=None):
    """
    - la réunion doit être terminée
    - création : gestionnaire ou participant (non refusé)
    - modification : gestionnaire ou auteur du PV
    """
    if not user.is_authenticated or reunion.statut != StatutReunion.TERMINEE:
        return False
    if est_gestionnaire(user):
        return True
    if not est_participant_actif(user, reunion):
        return False
    return pv is None or pv.redacteur_id == user.pk


def roles_utilisateur(user):
    if not user.is_authenticated:
        return []

    roles = []

    for rel in user._meta.related_objects:
        if rel.one_to_one and rel.parent_link:
            if hasattr(user, rel.get_accessor_name()):
                roles.append(rel.related_model.__name__.lower())

    return roles


# =========================================================
# PERMISSIONS GENERALES MEETINGS
# =========================================================

def est_gestionnaire(user):
    """
    Gestionnaire = Directeur ou Chef de Département.
    Utilisé pour les actions d'administration des réunions.
    """
    return any(
        "directeur" in role or "chefdepartement" in role
        for role in roles_utilisateur(user)
    )


# =========================================================
# PERMISSION CREATION / MODIFICATION REUNION
# =========================================================

def peut_gerer_reunions(user):
    """
    Les utilisateurs suivants peuvent créer/modifier une réunion :
    - Ingénieur
    - Chef de Département
    - Directeur
    """
    if not user.is_authenticated:
        return False

    return user.poste in [
        "ingenieur",
        "chefdepartement",
        "directeur",
    ]


def reunion_permission_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if not peut_gerer_reunions(request.user):
            raise PermissionDenied

        return view(request, *args, **kwargs)

    return wrapper


# =========================================================
# GESTIONNAIRES SEULEMENT
# =========================================================

def gestionnaire_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if not est_gestionnaire(request.user):
            raise PermissionDenied

        return view(request, *args, **kwargs)

    return wrapper