from django.contrib import admin
from .models import Ticket, Commentaire


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ("titre", "categorie", "priorite", "statut", "createur", "assigne_a", "date_creation")
    list_filter   = ("statut", "categorie", "priorite")
    search_fields = ("titre", "description")


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("ticket", "auteur", "date", "est_reponse_ingenieur")
