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

