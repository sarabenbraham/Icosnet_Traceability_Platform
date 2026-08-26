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

