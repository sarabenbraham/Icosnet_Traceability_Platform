from django.conf import settings
from django.db import models
from django.utils import timezone


class Ticket(models.Model):

    class Categorie(models.TextChoices):
        RESEAU    = "reseau",    "R\u00e9seau"
        MATERIEL  = "materiel",  "Mat\u00e9riel"
        LOGICIEL  = "logiciel",  "Logiciel"
        ACCES     = "acces",     "Acc\u00e8s / Droits"
        AUTRE     = "autre",     "Autre"

    class Priorite(models.TextChoices):
        FAIBLE   = "faible",   "Faible"
        MOYEN    = "moyen",    "Moyen"
        ELEVE    = "eleve",    "\u00c9lev\u00e9"
        CRITIQUE = "critique", "Critique"

    class Statut(models.TextChoices):
        OUVERT    = "ouvert",    "Ouvert"
        EN_COURS  = "en_cours",  "En cours"
        RESOLU    = "resolu",    "R\u00e9solu"
        FERME     = "ferme",     "Ferm\u00e9"

    titre       = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description du probl\u00e8me")
    categorie   = models.CharField(max_length=20, choices=Categorie.choices, default=Categorie.AUTRE)
    priorite    = models.CharField(max_length=10, choices=Priorite.choices, default=Priorite.MOYEN)
    statut      = models.CharField(max_length=10, choices=Statut.choices, default=Statut.OUVERT)

    createur    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets_crees",
        verbose_name="Cr\u00e9ateur"
    )
    assigne_a   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tickets_assignes",
        verbose_name="Assign\u00e9 \u00e0 (Ing\u00e9nieur)"
    )

    date_creation  = models.DateTimeField(auto_now_add=True)
    date_maj       = models.DateTimeField(auto_now=True)
    date_cloture   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"[{self.get_statut_display()}] {self.titre}"

    def clore(self):
        self.statut = self.Statut.FERME
        self.date_cloture = timezone.now()
        self.save(update_fields=["statut", "date_cloture"])

    @property
    def duree_ouverture(self):
        """Retourne le nombre de jours depuis la cr\u00e9ation."""
        delta = (timezone.now() - self.date_creation)
        return delta.days


class Commentaire(models.Model):
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="commentaires")
    auteur  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField(verbose_name="Commentaire")
    date    = models.DateTimeField(auto_now_add=True)
    est_reponse_ingenieur = models.BooleanField(default=False)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"Commentaire de {self.auteur} sur #{self.ticket_id}"


class Notification(models.Model):
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="helpdesk_notifications",
        verbose_name="Destinataire"
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Ticket associé"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Notification Help Desk"
        verbose_name_plural = "Notifications Help Desk"

    def __str__(self):
        return f"Notification pour {self.destinataire}: {self.titre}"
