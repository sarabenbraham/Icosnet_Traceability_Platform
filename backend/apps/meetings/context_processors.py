# context_processors.py
from .models import Participation, StatutParticipation, StatutReunion
from .permissions import est_gestionnaire, peut_gerer_reunions, roles_utilisateur


def meetings(request):
    user = request.user
    if not user.is_authenticated:
        return {}

    invitations = (
        Participation.objects.filter(utilisateur=user, statut=StatutParticipation.EN_ATTENTE)
        .exclude(reunion__statut__in=[StatutReunion.ANNULEE, StatutReunion.TERMINEE])
        .select_related("reunion")
        .order_by("reunion__date", "reunion__heure_debut")
    )

    roles = roles_utilisateur(user)

    return {
        "peut_gerer_reunions": peut_gerer_reunions(user),   # créer / modifier / inviter
        "est_gestionnaire": est_gestionnaire(user),          # supprimer / lieux
        "invitations_count": invitations.count(),
        "invitations_recentes": list(invitations[:5]),
        "is_directeur": "directeur" in roles,
        "is_chef": "chefdepartement" in roles,
    }