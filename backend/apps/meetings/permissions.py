from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def roles_utilisateur(user):
    if not user.is_authenticated:
        return []

    roles = []
    for rel in user._meta.related_objects:
        if rel.one_to_one and rel.parent_link:
            if hasattr(user, rel.get_accessor_name()):
                roles.append(rel.related_model.__name__.lower())
    return roles


def est_gestionnaire(user):
    return any("directeur" in r or "chef" in r for r in roles_utilisateur(user))

def gestionnaire_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not est_gestionnaire(request.user):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper
    