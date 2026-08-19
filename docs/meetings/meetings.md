# Documentation du Module Réunions (Meetings)

## 1. Description de l'Application

**ICOSNET DSI Platform - Module Réunions** est une application web interne permettant à la DSI d'organiser, de planifier et de tracer l'ensemble de ses réunions (techniques, projets, formations, urgences).
Ce module gère à la fois les lieux de réunion (salles) avec vérification de disponibilité, et les participations (invitations, confirmations, refus).

## 2. Types d'Utilisateurs

1. **Organisateurs (Membres DSI)** : Créent, modifient et annulent les réunions, réservent les salles et invitent des participants.
2. **Participants (Utilisateurs de la plateforme)** : Reçoivent les invitations et peuvent confirmer ou refuser leur présence.
3. **Administrateurs** : Gèrent le catalogue des lieux (salles) et leurs capacités.

## 3. Fonctionnalités Principales

* **Gestion des Lieux (Salles)** : Création et gestion des salles avec vérification automatique des conflits d'horaires (double réservation impossible).
* **Planification des Réunions** : Définition de l'objet, date, heure de début/fin, type et lieu.
* **Gestion des Participations** : Ajout de participants (rattachés aux utilisateurs Django) avec suivi de leur statut (En attente, Confirmée, Refusée).
* **Cycle de vie de la Réunion** : Statuts évolutifs (Créée, Planifiée, En cours, Terminée, Annulée).

## 4. Comment Lancer l'Application (Run)

Pour tester ou exécuter ce module en environnement de développement local :

1. **Ouvrir le terminal** à la racine du projet `Icosnet_Traceability_Platform`.
2. **Activer l'environnement virtuel** :
   * Windows : `.venv\Scripts\activate`
   * Linux/Mac : `source .venv/bin/activate`
3. **Appliquer les migrations** (si ce n'est pas déjà fait) : 
   `cd backend`
   `python manage.py makemigrations meetings`
   `python manage.py migrate`
4. **Lancer le serveur** : 
   `python manage.py runserver`
5. **Accéder à l'application** : L'accès par défaut se fera selon la configuration du `urls.py` principal (généralement via `http://127.0.0.1:8000/meetings/`).

## 5. Explication du Code (Architecture et Logique)

*(Voici les explications textuelles concernant l'architecture du code, pratiques pour accompagner vos éventuels schémas ou photos de diagrammes).*

### A. Modèles de Données (`models.py`)
Le module s'appuie sur trois entités principales liées par des clés étrangères (`ForeignKey`) :
* **`Lieu`** : Représente une salle. Il possède une méthode clé `est_disponible()` qui interroge la base de données pour vérifier s'il n'y a pas de conflit d'horaire avec une autre réunion déjà planifiée le même jour dans la même salle (vérification du chevauchement des heures).
* **`Reunion`** : Le cœur du module. Lors de la validation d'une réunion (via la méthode surchargée `clean()`), le modèle vérifie deux règles strictes :
  1. L'heure de fin doit être strictement postérieure à l'heure de début.
  2. La salle choisie doit être disponible (via l'appel de `lieu.est_disponible()`). Si la salle est prise, l'enregistrement est refusé (levée d'une erreur de validation).
* **`Participation`** : Table de liaison entre une `Reunion` et un `Participant` (Utilisateur Django). Elle dispose de méthodes métier `confirmer()` et `refuser()` pour changer le statut d'un participant et enregistrer la date et l'heure exactes de sa réponse. Elle possède également une contrainte d'unicité (`UniqueConstraint` sur BDD) pour éviter qu'une même personne ne soit invitée deux fois à la même réunion.

### B. Vues et Routage (`views.py` & `urls.py`)
Les vues sont organisées autour du modèle classique CRUD (Create, Read, Update, Delete) pour les 3 entités :
* Les vues de **Lieux** et de **Réunions** utilisent la méthode sécurisée `get_object_or_404()` pour la récupération des objets, évitant les crashs si une ressource est inexistante.
* Les vues de **Participations** (`participation_confirmer` et `participation_refuser`) sont très directes : elles gèrent les actions rapides de réponse aux invitations via des requêtes POST, appellent les méthodes métier du modèle, affichent un message de succès (via le framework Django Messages) puis redirigent l'utilisateur sur la page de détail de la réunion.
