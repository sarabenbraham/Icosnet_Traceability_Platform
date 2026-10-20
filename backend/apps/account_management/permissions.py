# -*- coding: utf-8 -*-

def _est_directeur_systeme(user):
    """
    Retourne True si l'utilisateur est un Ingénieur AVEC le rôle Directeur Système.
    """
    if not user or not user.is_authenticated:
        return False
    try:
        from apps.users.models import Ingenieur
        ing = Ingenieur.objects.get(pk=user.pk)
        return bool(ing.est_directeur_systeme)
    except Exception:
        return bool(getattr(user, "est_directeur_systeme", False))
