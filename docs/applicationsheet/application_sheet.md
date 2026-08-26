# Documentation du Module Fiche Applicative

## 1. Description de l'Application

**ICOSNET DSI Platform - Module Fiche Applicative** est une application web interne en Python/Django développée pour la Direction des Systèmes d'Information (DSI). L'objectif est d'améliorer la traçabilité, de centraliser et d'historiser les informations techniques et fonctionnelles relatives aux applications gérées par la DSI.

Ce module offre aux équipes de la DSI la possibilité de gérer un dossier applicatif complet. Chaque fiche est structurée en plusieurs sections : infrastructure, contrats, accès, développement, sauvegarde, etc.

## 2. Types d'Utilisateurs

Dans le contexte de la DSI, les utilisateurs se divisent en plusieurs profils :
1. **Ingénieurs / Développeurs** : Créent et mettent à jour les fiches applicatives (rattachés via le champ `ingenieur`).
2. **Managers de Départements** : Consultent les fiches pour le suivi budgétaire et fonctionnel (liés via `departements`).
3. **Administrateurs Système / Réseau** : Renseignent et valident les sections techniques (Infrastructure, Flux, Sauvegarde, Intégration).
4. **Validateurs (Chefs de projet / DSI)** : Examinent les fiches en statut "En validation" pour les approuver ou les refuser.

## 3. Fonctionnalités Principales

* **Gestion du cycle de vie des fiches** : Statuts (Brouillon, En attente, En validation, Validée, Refusée).
* **Création centralisée** : Un formulaire unique pour créer la fiche et toutes ses dépendances techniques.
* **Consultation et Historisation** : Vue détaillée de l'ensemble du dossier d'une application.
* **Suppression sécurisée** : Suppression en cascade de la fiche et de ses sous-sections.

## 4. Comment Lancer l'Application (Run)

Pour lancer le module en environnement de développement local :

1. **Cloner le projet** et ouvrir le terminal dans le dossier racine `Icosnet_Traceability_Platform`.
2. **Activer l'environnement virtuel** :
   * Windows : `.venv\Scripts\activate`
   * Mac/Linux : `source .venv/bin/activate`
3. **Installer les dépendances** : 
   `pip install -r requirements.txt`
4. **Appliquer les migrations** (création des tables de la BDD) : 
   `cd backend`
   `python manage.py migrate`
5. **Démarrer le serveur Django** : 
   `python manage.py runserver`
6. **Accéder à l'application** via votre navigateur Web : `http://127.0.0.1:8000/`

