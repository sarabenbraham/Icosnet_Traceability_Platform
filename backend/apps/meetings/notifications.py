from django.core.mail import send_mail
from django.urls import reverse


def notifier_invitation(request, participation):
    user = participation.utilisateur
    if not user or not user.email:
        return False

    reunion = participation.reunion
    lieu = reunion.lieu.nom_salle if reunion.lieu else "À définir"
    lien = request.build_absolute_uri(reverse("meetings:mes_invitations"))
    horaire = f"{reunion.heure_debut:%H:%M}"
    if reunion.heure_fin:
        horaire += f" – {reunion.heure_fin:%H:%M}"

    corps = (
        f"Bonjour {user.get_full_name() or user.get_username()},\n\n"
        f"Vous êtes invité(e) à la réunion « {reunion.objet} ».\n\n"
        f"Date : {reunion.date:%d/%m/%Y}\n"
        f"Horaire :  {horaire}\n"
        f"Lieu : {lieu}\n"
        f"Organisateur : {reunion.organisateur}\n\n"
        f"Confirmez ou refusez votre participation ici : {lien}\n"
    )
    send_mail(
        subject=f"Invitation : {reunion.objet}",
        message=corps,
        from_email=None,  # utilise DEFAULT_FROM_EMAIL
        recipient_list=[user.email],
        fail_silently=True,
    )
    return True