from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentaireForm, StatutForm, TicketForm
from .models import Commentaire, Ticket


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
    return hasattr(user, "ingenieur") or user.poste == "ingenieur"


@login_required
def ticket_list(request):
    qs = Ticket.objects.select_related("createur", "assigne_a")

    # Les ing\u00e9nieurs voient tous les tickets ; les autres voient les leurs
    if not _est_agent_helpdesk(request.user):
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

    # Stats pour la barre du haut
    tous = Ticket.objects.all() if _est_agent_helpdesk(request.user) else Ticket.objects.filter(createur=request.user)
    stats = {
        "total":    tous.count(),
        "ouverts":  tous.filter(statut=Ticket.Statut.OUVERT).count(),
        "en_cours": tous.filter(statut=Ticket.Statut.EN_COURS).count(),
        "resolus":  tous.filter(statut=Ticket.Statut.RESOLU).count(),
    }

    return render(request, "helpdesk/ticket_list.html", {
        "tickets":          qs,
        "titre":            "Help Desk",
        "sous_titre":       "Suivi des demandes techniques",
        "statuts":          Ticket.Statut.choices,
        "categories":       Ticket.Categorie.choices,
        "priorites":        Ticket.Priorite.choices,
        "filtre_statut":    statut,
        "filtre_categorie": categorie,
        "filtre_priorite":  priorite,
        "q":                q,
        "stats":            stats,
        "est_ingenieur":    _est_ingenieur(request.user),
        "est_helpdesk":     _est_agent_helpdesk(request.user),
    })


@login_required
def ticket_create(request):
    form = TicketForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.createur = request.user
        ticket.save()
        messages.success(request, "\u2705 Votre ticket a \u00e9t\u00e9 soumis avec succ\u00e8s.")
        return redirect("helpdesk:detail", pk=ticket.pk)

    return render(request, "helpdesk/ticket_form.html", {
        "form":       form,
        "titre":      "Nouveau ticket",
        "sous_titre": "Signaler un probl\u00e8me technique",
    })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("createur", "assigne_a"), pk=pk)

    # Seul le cr\u00e9ateur ou un ing\u00e9nieur peut voir le ticket
    if ticket.createur != request.user and not _est_agent_helpdesk(request.user):
        messages.error(request, "Acc\u00e8s refus\u00e9.")
        return redirect("helpdesk:liste")

    commentaires   = ticket.commentaires.select_related("auteur").all()
    comment_form   = CommentaireForm()
    statut_form    = StatutForm(instance=ticket) if _est_agent_helpdesk(request.user) else None

    if request.method == "POST":
        action = request.POST.get("action")

        # ── Ing\u00e9nieur : changer statut / assignation ──
        if action == "statut" and _est_agent_helpdesk(request.user):
            statut_form = StatutForm(request.POST, instance=ticket)
            if statut_form.is_valid():
                t = statut_form.save(commit=False)
                if t.statut == Ticket.Statut.FERME:
                    t.clore()
                else:
                    t.save()
                messages.success(request, "Statut mis \u00e0 jour.")
                return redirect("helpdesk:detail", pk=pk)

        # ── Ajouter un commentaire ──
        elif action == "commentaire":
            comment_form = CommentaireForm(request.POST)
            if comment_form.is_valid():
                c = comment_form.save(commit=False)
                c.ticket = ticket
                c.auteur = request.user
                c.est_reponse_ingenieur = _est_agent_helpdesk(request.user)
                c.save()
                messages.success(request, "Commentaire ajout\u00e9.")
                return redirect("helpdesk:detail", pk=pk)

    return render(request, "helpdesk/ticket_detail.html", {
        "ticket":        ticket,
        "commentaires":  commentaires,
        "comment_form":  comment_form,
        "statut_form":   statut_form,
        "titre":         f"Ticket #{ticket.pk}",
        "sous_titre":    ticket.titre,
        "est_ingenieur": _est_ingenieur(request.user),
        "est_helpdesk":  _est_agent_helpdesk(request.user),
    })
