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

## 5. Explication du Code (Architecture et Logique)

*(Les diagrammes ayant été insérés en format image, voici l'explication textuelle détaillant l'architecture du code, les modèles et les workflows).*

### A. Les Modèles de Données (`models.py`)
Le modèle de données est pensé pour être modulaire et repose sur une entité principale : `FicheApplicative`.
* **Relation OneToOne (1:1)** : Toutes les autres entités (comme `Contrat`, `Infrastructure`, `UtilisateurAcces`, `Sauvegarde`) sont rattachées à la `FicheApplicative` via un `OneToOneField`. Cela garantit qu'une application ne possède qu'une seule configuration d'infrastructure, un seul contrat principal, etc.
* **Suppression en cascade (`on_delete=models.CASCADE`)** : Cette contrainte assure que si la `FicheApplicative` principale est supprimée, toutes les sections associées (infrastructure, contrat, flux) sont automatiquement effacées de la base de données, évitant ainsi les données orphelines.
* **Énumérations (Enums)** : Pour garantir l'intégrité des données saisies (ex: les statuts, le type d'infrastructure ou les environnements), le modèle utilise les `models.TextChoices` de Django. Par exemple, le statut est strictement limité à `BROUILLON`, `VALIDEE`, etc.

### B. Logique des Vues et des Transactions (`views.py`)
Les vues gèrent la logique métier et le traitement des requêtes de l'utilisateur :
* **Consultation optimisée (`fiche_list`, `fiche_detail`)** : Les vues utilisent les méthodes `select_related()` et `prefetch_related()` de l'ORM Django. Cela permet d'optimiser les requêtes SQL en chargeant en avance les données liées (l'ingénieur et les départements rattachés) sans surcharger la base de données avec des requêtes redondantes (problème du N+1 queries).
* **Création sécurisée (`create_fiche_applicative`)** : Le processus de création d'une fiche complète implique l'enregistrement de 10 objets différents (Modèles) en même temps. Pour garantir que la base de données reste cohérente, le code utilise **`transaction.atomic()`**.
  * **Si tout est valide**, l'ensemble des données (Fiche + Infrastructure + Contrat...) est validé et inséré dans la base de données de manière globale.
  * **En cas d'erreur** (ex: coupure ou une sous-section invalide), un *rollback* est effectué. L'opération est totalement annulée, évitant de se retrouver avec une fiche "à moitié" créée.

### C. Le Workflow de Validation (Diagramme d'Activité)
Le cycle de vie d'une fiche suit une logique métier précise à travers son champ `statut` :
1. **Initialisation** : L'ingénieur saisit les informations. Il peut enregistrer la fiche en `BROUILLON` si elle est incomplète.
2. **Soumission** : La fiche passe au statut `EN_ATTENTE` lorsqu'elle est prête, puis `EN_VALIDATION` lorsqu'un valideur technique s'en charge.
3. **Décision** : Le responsable de validation prend une décision finale : 
   * **Acceptation** : La fiche est marquée comme `VALIDEE`.
   * **Rejet** : La fiche est marquée comme `REFUSEE` et repart au statut brouillon pour permettre les corrections par l'ingénieur.
