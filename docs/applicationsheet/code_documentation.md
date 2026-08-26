# Documentation Technique : Application Sheet

Ce document détaille l'architecture et les choix techniques effectués pour l'application `application_sheet`. Le but de cette application est de recenser et de gérer toutes les fiches descriptives des applications du SI (Système d'Information), de leur infrastructure à leurs flux réseaux.

## 1. Modèles (`models/`)

Pour des raisons de maintenabilité et de lisibilité, le fichier monolithique `models.py` a été scindé en un **package de modèles** (dossier `models/`). Chaque entité métier possède son propre fichier Python, et toutes les entités sont ré-exportées via le fichier `__init__.py`. Cela permet aux autres parties de l'application (formulaires, vues) de fonctionner sans aucune modification des imports.

### Fichiers de modèles :
- **`fiche_applicative.py`** : Définit le modèle principal `FicheApplicative`. C'est le cœur de l'application. 
  - *Choix technique* : Utilisation de `MultiSelectField` (package externe `django-multiselectfield`) pour le champ `domaine_fonctionnel`. Cela permet à l'utilisateur de sélectionner plusieurs domaines (RH, COMMERCIAL, etc.) sans avoir à créer une table de base de données dédiée pour les domaines, préservant ainsi la simplicité des `TextChoices`.
- **`contrat.py`, `infrastructure.py`, `utilisateur_acces.py`, `developpement.py`, `module_metier.py`, `stockage.py`, `integration.py`, `flux_application.py`, `sauvegarde.py`, `intervention.py`** : Tous ces modèles représentent des "facettes" ou des sections de la Fiche Applicative.
  - *Choix technique* : Ils sont tous liés au modèle principal `FicheApplicative` via une relation **`OneToOneField`**. Cela garantit qu'une fiche applicative ne possède qu'une seule infrastructure, un seul contrat, etc. C'est l'approche idéale pour modéliser des formulaires à onglets ou des sections détaillées.
  - *Validation (`clean()`)* : Chaque modèle contient une méthode `clean()` sur-mesure pour s'assurer de la cohérence des données (ex: Si le type d'infrastructure est CLOUD, le type de cloud devient obligatoire).

## 2. Formulaires (`forms.py`)

Les formulaires sont construits avec `forms.ModelForm` pour générer automatiquement les champs HTML basés sur les modèles.

- *Choix technique* : Utilisation des `widgets` pour améliorer l'expérience utilisateur (ex: `forms.CheckboxSelectMultiple()` pour les champs `departements`, et utilisation de `Textarea` pour forcer des zones de texte plus grandes sur les descriptions).
- Un formulaire principal `FicheApplicativeForm` est utilisé pour les données générales, et des sous-formulaires (ex: `InfrastructureForm`, `ContratForm`) sont utilisés pour les entités One-to-One.

## 3. Vues (`views.py`)

Les vues coordonnent l'affichage et le traitement des formulaires complexes de la fiche applicative.

- **`create_fiche_applicative` / `fiche_update`** : Ces vues sont particulièrement complexes car elles doivent traiter de multiples formulaires en une seule soumission HTTP POST (la Fiche Principale + ses 10 entités enfants).
  - *Choix technique* : L'utilisation de `@transaction.atomic` est cruciale ici. Elle assure que si la sauvegarde d'un des sous-formulaires (ex: `Contrat`) échoue, l'ensemble de la création (y compris la `FicheApplicative` principale) est annulé (rollback). Cela évite d'avoir des fiches orphelines ou incomplètes en base de données.
- **Optimisation (N+1 queries)** : Les vues de type `fiche_list` ou `fiche_detail` utilisent systématiquement `select_related()` (pour les ForeignKey comme l'ingénieur) et `prefetch_related()` (pour les ManyToMany comme les départements). Cela limite drastiquement le nombre de requêtes SQL générées lors de l'affichage de la liste des fiches.
- **Sécurité** : Toutes les vues de manipulation des fiches sont (ou doivent être) protégées pour s'assurer que seuls les utilisateurs autorisés peuvent créer, éditer ou supprimer des données.

## Résumé
L'application `application_sheet` est le module le plus complexe en base de données de la plateforme. La décision de découper les modèles en plusieurs fichiers (`models/`) et l'utilisation de transactions atomiques (`transaction.atomic()`) dans les vues sont les clés de voûte de sa stabilité et de sa maintenabilité.
