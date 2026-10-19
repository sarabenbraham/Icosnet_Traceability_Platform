from .models import Notification


def notifications_fiches(request):
    user = request.user
    if not user.is_authenticated:
        return {}

    non_lues = (
        Notification.objects
        .filter(destinataire=user, lue=False)
        .select_related("fiche")
    )

    return {
        "notifications_fiches_count": non_lues.count(),
        "notifications_fiches": list(non_lues[:5]),
    }