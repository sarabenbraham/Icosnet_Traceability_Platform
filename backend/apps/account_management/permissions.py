# -*- coding: utf-8 -*-

def _est_directeur_systeme(user):
    """
    Retourne True si l'utilisateur est un Directeur AVEC le rôle Directeur Système.
    """
    if not user or not user.is_authenticated:
        return False
    try:
        from apps.users.models import Directeur
        d = Directeur.objects.get(pk=user.pk)
        return bool(d.est_directeur_systeme)
    except Exception:
        return bool(getattr(user, "est_directeur_systeme", False))
