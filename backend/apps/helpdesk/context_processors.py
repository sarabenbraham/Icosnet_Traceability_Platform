# -*- coding: utf-8 -*-

def helpdesk_context(request):
    user = request.user
    if not user.is_authenticated:
        return {}

    from .models import Notification
    from .views import _est_agent_helpdesk

    is_hd = _est_agent_helpdesk(user)
    unread_notifs = Notification.objects.filter(destinataire=user, lu=False).select_related("ticket")[:6]
    unread_count = Notification.objects.filter(destinataire=user, lu=False).count()

    return {
        "is_agent_helpdesk": is_hd,
        "helpdesk_unread_count": unread_count,
        "helpdesk_notifications": list(unread_notifs),
    }
