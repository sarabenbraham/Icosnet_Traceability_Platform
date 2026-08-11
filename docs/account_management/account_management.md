# Documentation du Module Gestion de Comptes (Account Management)

## 1. Description de l'Application

**ICOSNET DSI Platform - Module Gestion de Comptes** est un module central de la plateforme permettant de gérer les comptes utilisateurs et l'authentification.
Ce module assure la sécurité des accès en gérant les mots de passe (avec hachage), les dates d'expiration des comptes, et leur activation/désactivation, garantissant ainsi un contrôle strict des accès à la DSI.

## 2. Types d'Utilisateurs

Dans ce contexte, les utilisateurs sont gérés de la manière suivante :
1. **Administrateurs (DSI)** : Peuvent créer, activer ou désactiver les comptes, et définir les dates d'expiration.
2. **Utilisateurs Finaux** : Se connectent avec leur email et mot de passe, soumis aux règles d'expiration.

## 3. Fonctionnalités Principales

* **Sécurité des mots de passe** : Hachage automatique des mots de passe (méthodes `set_password` et `check_password`).
* **Gestion du cycle de vie des comptes** : Statuts d'activation (Actif / Désactivé).
* **Contrôle d'expiration** : Vérification de la date limite d'utilisation d'un compte avec désactivation automatique ou marquage en tant qu'expiré (`verifier_expiration`).

## 4. Comment Lancer l'Application (Run)

Pour lancer le projet et activer ce module en environnement de développement local :

1. **Ouvrir le terminal** dans le dossier racine `Icosnet_Traceability_Platform`.
2. **Activer l'environnement virtuel** :
   * Windows : `.venv\Scripts\activate`
   * Mac/Linux : `source .venv/bin/activate`
3. **Appliquer les migrations** (création de la table `Compte` dans la BDD) : 
   `cd backend`
   `python manage.py makemigrations account_management`
   `python manage.py migrate`
4. **Démarrer le serveur Django** : 
   `python manage.py runserver`
5. **Accès** : L'interface d'administration est disponible sur `http://127.0.0.1:8000/`.

## 5. Explication du Code (Architecture et Logique)

*(Les diagrammes ayant potentiellement été insérés en format image, voici l'explication textuelle du fonctionnement du module)*

### A. Modèle de Données (`Compte` - `models.py`)
Le modèle de données repose sur l'entité `Compte` :
* **Relation avec l'Utilisateur** : Il est rattaché au modèle utilisateur de base de Django (`AUTH_USER_MODEL`) via un **OneToOneField**. Cela signifie que chaque profil utilisateur possède une extension de compte spécifique et sécurisée au sein de l'application.
* **Champs de sécurité** : 
  * `mot_de_passe` : Stocke le mot de passe de façon cryptée.
  * `email_connexion` : Sert d'identifiant unique.
  * `statut` : Géré par des `TextChoices` (Enum) pour s'assurer que le statut est strictement `ACTIF` ou `DESACTIVE`.
  * `date_expiration` et `expire` : Gèrent la validité temporelle de l'accès de l'utilisateur.

### B. Méthodes Intégrées (Logique Métier)
Le modèle contient lui-même la logique de sécurité essentielle, sans s'appuyer uniquement sur les vues :
* **`set_password()` et `check_password()`** : Ces fonctions font appel aux utilitaires cryptographiques de Django (`make_password`, `check_password`). Elles garantissent qu'aucun mot de passe n'est stocké ou vérifié en clair.
* **`verifier_expiration()`** : Une méthode vitale permettant de vérifier si la date actuelle dépasse la `date_expiration` définie pour un compte. 
  * Si la date est dépassée et que le compte est encore marqué comme actif, la fonction passe automatiquement le flag `expire` à `True`, le sauvegarde dans la base de données via `update_fields`, et retourne `True` pour signaler que le compte est désuet.
