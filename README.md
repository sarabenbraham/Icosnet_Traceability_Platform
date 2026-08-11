# ICOSNET DSI Platform - Plateforme de Traçabilité

## Description du Projet

**ICOSNET DSI Platform** est une application web interne développée spécifiquement pour la Direction des Systèmes d'Information (DSI). L'objectif principal de cette plateforme est d'améliorer la traçabilité, de structurer, de centraliser et d'historiser les processus IT internes.

La plateforme permet la gestion des activités importantes de la DSI, notamment :
* La gestion des fiches applicatives (Dossier complet de chaque application gérée).
* La gestion des comptes génériques.
* La traçabilité des réunions et des décisions techniques.
* Le suivi du matériel (Hardware tracking).

L'architecture du projet repose sur le framework **Django** (Python) et utilise une structure modulaire, permettant de séparer clairement les différents modules métiers (ex: `application_sheet`, `users`, `organization`) et d'assurer la scalabilité de l'application.

## Architecture et Technologies

* **Backend** : Python 3, Django
* **Base de données** : SQLite (pour le développement local), PostgreSQL (prévu pour la production)
* **Frontend** : Django Templates (rendu côté serveur), HTML, CSS
* **Outils** : Git, GitHub, Docker (prévu pour le déploiement)

---

## Guide d'Installation (Environnement de Développement)

Suivez ces instructions pour installer et lancer le projet sur votre environnement local.

### 1. Cloner le dépôt

Clonez le projet sur votre machine locale et accédez au dossier principal :

```bash
git clone <url_du_depot>
cd Icosnet_Traceability_Platform
```

### 2. Créer l'environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet. Assurez-vous d'être dans le dossier contenant le fichier `requirements.txt` (ou le dossier `backend` s'il s'y trouve).

```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel

* **Sous Windows :**
  ```bash
  .venv\Scripts\activate
  ```

* **Sous macOS et Linux :**
  ```bash
  source .venv/bin/activate
  ```

### 4. Installer les dépendances

Installez toutes les bibliothèques requises définies dans le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

*(Note : Si le fichier `requirements.txt` se trouve dans le répertoire racine, exécutez la commande depuis la racine. S'il se trouve dans `backend/`, naviguez d'abord vers `cd backend/`)*

### 5. Appliquer les migrations de base de données

Naviguez vers le dossier contenant `manage.py` (habituellement le dossier `backend`) pour configurer la base de données SQLite :

```bash
cd backend
python manage.py migrate
```

### 6. Lancer le serveur de développement

Démarrez le serveur local :

```bash
python manage.py runserver
```

L'application sera alors accessible via votre navigateur Web à l'adresse suivante :
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Structure de la Documentation

La documentation technique détaillée (diagrammes de classes, diagrammes de séquences, description de l'application et workflows) se trouve dans le dossier `docs/` :

* `docs/applicationsheet/application_sheet.md` : Description de l'application, types d'utilisateurs, fonctionnalités et workflow d'activité.
* `docs/applicationsheet/technical_diagrams.md` : Diagrammes de classes, énumérations, diagrammes de séquence et endpoints.

**Gestion de Comptes (Account Management)**
* `docs/account_management/account_management.md` : Description du module, sécurité, et workflows.
* `docs/account_management/technical_diagrams.md` : Diagrammes de classes, diagrammes de séquences (Hachage et Expiration).

## Contributeurs

* Sara Benbraham
* Farah Laggoune
