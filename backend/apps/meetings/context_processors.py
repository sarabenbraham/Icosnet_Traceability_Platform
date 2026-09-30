from .models import Participation, StatutParticipation, StatutReunion
from .permissions import est_gestionnaire, roles_utilisateur


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
        "peut_gerer_reunions": any("directeur" in r or "chefdepartement" in r for r in roles),
        "invitations_count": invitations.count(),
        "invitations_recentes": list(invitations[:5]),
        "is_directeur": "directeur" in roles,
        "is_chef": "chefdepartement" in roles,
    }