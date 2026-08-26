# Documentation Technique : Meetings

Ce document détaille l'architecture et les choix techniques effectués pour l'application `meetings`. Le but de cette application est de gérer la planification des réunions, les lieux (physiques ou virtuels), et d'assurer le suivi des participations (invitations, confirmations, refus).

## 1. Modèles (`models.py`)

La base de données s'articule autour de trois modèles principaux qui interagissent entre eux :

- **`Lieu`** : Représente l'endroit de la réunion.
  - *Choix technique* : Contient un champ `est_virtuel` (booléen) et un `lien_visio` optionnel. Cela permet de gérer de manière unifiée à la fois les salles de conférence physiques de l'entreprise et les réunions Teams/Zoom.
- **`Reunion`** : Le modèle central. Il lie un `Lieu` (ForeignKey) et un `organisateur` (lié au modèle `User` de Django via ForeignKey).
  - *Validation* : La méthode `clean()` est implémentée pour s'assurer que la `date_fin` est toujours postérieure à la `date_debut`. C'est un point de contrôle crucial au niveau de la base de données pour empêcher la création de réunions impossibles temporellement.
- **`Participation`** : Modèle de jointure (table intermédiaire) entre un `User` (le participant) et une `Reunion`.
  - *Statuts* : Il utilise des `TextChoices` pour le statut de la réponse (EN_ATTENTE, ACCEPTE, REFUSE).
  - *Contrainte d'unicité* : Utilisation de `unique_together = ('reunion', 'participant')` (ou `UniqueConstraint`) pour garantir qu'un utilisateur ne peut pas être invité deux fois à la même réunion, ce qui empêcherait les doublons dans les statistiques de présence.

## 2. Formulaires (`forms.py`)

Les formulaires servent de pont sécurisé entre les interfaces HTML et les modèles.

- **`ReunionForm`** : Utilise le composant de date/heure natif du navigateur grâce à la définition spécifique de widgets (`forms.DateTimeInput(attrs={'type': 'datetime-local'})`). Cela permet d'avoir un calendrier popup pour la sélection des dates sans recourir à du JavaScript externe complexe.
- **`LieuForm`** : Un formulaire basique qui permet à l'administration ou aux organisateurs d'ajouter de nouvelles salles ou de nouveaux liens virtuels réutilisables.

## 3. Vues (`views.py`)

Les vues de `meetings` orchestrent une logique métier orientée vers l'action de l'utilisateur (accepter/refuser une invitation).

- **Sécurité et Authentification (`@login_required`)** : Le choix technique majeur de ce fichier est l'application du décorateur `@login_required` sur l'intégralité des fonctions. Cela verrouille complètement le module : impossible de voir les réunions ou d'y répondre sans être un membre du personnel connecté.
- **Vues CRUD Standards (`reunion_list`, `lieu_create`, etc.)** : Les requêtes sont optimisées avec `select_related('lieu', 'organisateur')` pour charger les données associées en une seule requête SQL.
- **Vues d'Actions (`participation_confirmer`, `participation_refuser`)** : 
  - Ces vues sont des "endpoints d'action". Contrairement aux vues classiques qui retournent des pages HTML complètes (templates), elles modifient l'état d'un objet `Participation` en changeant son statut, le sauvegardent, puis effectuent une redirection (`redirect`) vers le détail de la réunion.
  - *Avantage* : Ce pattern (Post/Redirect/Get) empêche la re-soumission accidentelle du formulaire si l'utilisateur rafraîchit la page après avoir cliqué sur "Accepter".

## Résumé
L'application `meetings` se distingue par sa forte gestion des contraintes logiques temporelles (dans `models.py`) et par l'utilisation de vues d'action sécurisées qui modifient les états de participation. Le tout est encapsulé par le système d'authentification pour garantir la confidentialité des agendas internes.
