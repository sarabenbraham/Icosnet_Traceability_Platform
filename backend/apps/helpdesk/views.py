from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentaireForm, StatutForm, TicketForm
from .models import Commentaire, Notification, Ticket


def _est_agent_helpdesk(user):
    """
    Retourne True si l'utilisateur est un ingénieur AVEC le rôle Help Desk.
    """
    try:
        from apps.users.models import Ingenieur
        ing = Ingenieur.objects.get(pk=user.pk)
        return ing.est_helpdesk
    except Exception:
        return False


def _est_ingenieur(user):
    """Retourne True si l'utilisateur est un ingénieur (avec ou sans rôle Help Desk)."""
    return hasattr(user, "ingenieur") or getattr(user, "poste", "") == "ingenieur"


@login_required
def ticket_list(request):
    est_hd = _est_agent_helpdesk(request.user)
    qs = Ticket.objects.select_related("createur", "assigne_a")

    # STRICT ISOLATION :
    # Seul l'agent Help Desk voit toutes les réclamations de la DSI.
    # Tout autre utilisateur ne voit STRICTEMENT QUE ses propres réclamations.
    if not est_hd:
        qs = qs.filter(createur=request.user)

    # Filtres
    statut    = request.GET.get("statut", "")
    categorie = request.GET.get("categorie", "")
    priorite  = request.GET.get("priorite", "")
    q         = request.GET.get("q", "").strip()

    if statut:
        qs = qs.filter(statut=statut)
    if categorie:
        qs = qs.filter(categorie=categorie)
    if priorite:
        qs = qs.filter(priorite=priorite)
    if q:
        qs = qs.filter(Q(titre__icontains=q) | Q(description__icontains=q))

    # Stats
    tous = Ticket.objects.all() if est_hd else Ticket.objects.filter(createur=request.user)
    stats = {
        "total":    tous.count(),
        "ouverts":  tous.filter(statut=Ticket.Statut.OUVERT).count(),
        "en_cours": tous.filter(statut=Ticket.Statut.EN_COURS).count(),
        "resolus":  tous.filter(statut=Ticket.Statut.RESOLU).count(),
    }

    # Notifications non lues pour cet utilisateur
    notifs_non_lues = Notification.objects.filter(destinataire=request.user, lu=False).select_related("ticket")[:5]

    titre = "Help Desk – Supervision DSI" if est_hd else "Mes Réclamations"
    sous_titre = (
        "File d'attente de toutes les réclamations techniques à traiter"
        if est_hd
        else "Suivi de vos signalements de problèmes et des réponses du Help Desk"
    )

    return render(request, "helpdesk/ticket_list.html", {
        "tickets":          qs,
        "titre":            titre,
        "sous_titre":       sous_titre,
        "statuts":          Ticket.Statut.choices,
        "categories":       Ticket.Categorie.choices,
        "priorites":        Ticket.Priorite.choices,
        "filtre_statut":    statut,
        "filtre_categorie": categorie,
        "filtre_priorite":  priorite,
        "q":                q,
        "stats":            stats,
        "est_ingenieur":    _est_ingenieur(request.user),
        "est_helpdesk":     est_hd,
        "notifs_non_lues":  notifs_non_lues,
    })


@login_required
def ticket_create(request):
    form = TicketForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.createur = request.user
        ticket.save()

        # NOTIFICATION POUR L'AGENT HELP DESK :
        from apps.users.models import Ingenieur
        agents_hd = Ingenieur.objects.filter(est_helpdesk=True)
        demandeur_nom = request.user.get_full_name() or request.user.username

        for agent in agents_hd:
            Notification.objects.create(
                destinataire=agent,
                ticket=ticket,
                titre=f"Nouvelle réclamation #{ticket.pk}",
                message=f"{demandeur_nom} a signalé un problème : '{ticket.titre}'.",
            )

        messages.success(request, "✅ Votre réclamation a été transmise à l'Agent Help Desk. Vous serez notifié dès sa prise en charge.")
        return redirect("helpdesk:detail", pk=ticket.pk)

    return render(request, "helpdesk/ticket_form.html", {
        "form":       form,
        "titre":      "Signaler un problème technique",
        "sous_titre": "Ouvrir un ticket auprès de l'Agent Help Desk",
    })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("createur", "assigne_a"), pk=pk)
    est_hd = _est_agent_helpdesk(request.user)

    # STRICT ISOLATION :
    # Seul le créateur ou l'Agent Help Desk peut accéder au ticket.
    if ticket.createur != request.user and not est_hd:
        messages.error(request, "Accès refusé : vous ne pouvez consulter que vos propres réclamations.")
        return redirect("helpdesk:liste")

    # Marquer les notifications de ce ticket comme lues pour l'utilisateur actuel
    Notification.objects.filter(destinataire=request.user, ticket=ticket, lu=False).update(lu=True)

    commentaires   = ticket.commentaires.select_related("auteur").all()
    comment_form   = CommentaireForm()
    statut_form    = StatutForm(instance=ticket) if est_hd else None

    if request.method == "POST":
        action = request.POST.get("action")

        # ── SEUL L'AGENT HELP DESK PEUT CHANGER LE STATUT / ASSIGNER ──
        if action == "statut" and est_hd:
            statut_form = StatutForm(request.POST, instance=ticket)
            if statut_form.is_valid():
                t = statut_form.save(commit=False)
                if t.statut == Ticket.Statut.FERME:
                    t.clore()
                else:
                    t.save()

                # NOTIFICATION AU DEMANDEUR (Créateur du ticket)
                Notification.objects.create(
                    destinataire=ticket.createur,
                    ticket=ticket,
                    titre=f"Mise à jour de votre ticket #{ticket.pk}",
                    message=f"L'Agent Help Desk a mis à jour votre réclamation '{ticket.titre}'. Nouveau statut : {ticket.get_statut_display()}.",
                )

                messages.success(request, "Statut du ticket mis à jour avec succès.")
                return redirect("helpdesk:detail", pk=pk)

        # ── AJOUTER UN COMMENTAIRE ──
        elif action == "commentaire":
            comment_form = CommentaireForm(request.POST)
            if comment_form.is_valid():
                c = comment_form.save(commit=False)
                c.ticket = ticket
                c.auteur = request.user
                c.est_reponse_ingenieur = est_hd
                c.save()

                auteur_nom = request.user.get_full_name() or request.user.username

                if est_hd:
                    # L'Agent Help Desk a répondu -> NOTIFIER LE CRÉATEUR
                    if ticket.createur != request.user:
                        Notification.objects.create(
                            destinataire=ticket.createur,
                            ticket=ticket,
                            titre=f"Réponse Help Desk sur votre ticket #{ticket.pk}",
                            message=f"L'Agent Help Desk ({auteur_nom}) a répondu à votre problème : '{ticket.titre}'.",
                        )
                else:
                    # Le demandeur a répondu -> NOTIFIER L'AGENT ASSIGNÉ OU L'ÉQUIPE HELP DESK
                    from apps.users.models import Ingenieur
                    destinataires = [ticket.assigne_a] if ticket.assigne_a else list(Ingenieur.objects.filter(est_helpdesk=True))
                    for dest in destinataires:
                        if dest and dest != request.user:
                            Notification.objects.create(
                                destinataire=dest,
                                ticket=ticket,
                                titre=f"Nouveau message sur la réclamation #{ticket.pk}",
                                message=f"{auteur_nom} a répondu sur le ticket '{ticket.titre}'.",
                            )

                messages.success(request, "Votre message a été envoyé.")
                return redirect("helpdesk:detail", pk=pk)

    return render(request, "helpdesk/ticket_detail.html", {
        "ticket":        ticket,
        "commentaires":  commentaires,
        "comment_form":  comment_form,
        "statut_form":   statut_form,
        "titre":         f"Ticket #{ticket.pk}",
        "sous_titre":    ticket.titre,
        "est_ingenieur": _est_ingenieur(request.user),
        "est_helpdesk":  est_hd,
    })
