# Documentation Technique : Account Management

Ce document détaille l'architecture et les choix techniques effectués pour l'application `account_management`. Le but de cette application est de gérer le cycle de vie des comptes utilisateurs, leurs statuts et les mots de passe.

## 1. Modèles (`models.py`)

Le modèle central est `Compte`. Il est conçu pour étendre le modèle d'authentification natif de Django (`AUTH_USER_MODEL`) grâce à une relation **OneToOneField**.

### Pourquoi cette approche ?
- **Séparation des responsabilités** : Le modèle `User` de Django gère l'authentification standard (session, permissions). Le modèle `Compte` gère les règles métiers spécifiques à Icosnet (dates d'expiration, statut actif/désactivé).
- **Sécurité et Hachage** : Le modèle inclut ses propres méthodes `set_password` et `check_password` pour hacher les mots de passe de manière sécurisée en utilisant `make_password` de Django. Cela permet de garder une trace locale des mots de passe métier tout en utilisant les outils cryptographiques robustes de Django.
- **Logique d'expiration** : La méthode `verifier_expiration()` automatise la désactivation d'un compte si la date courante dépasse la `date_expiration`. 

## 2. Formulaires (`forms.py`)

Les formulaires permettent de valider et de lier les données soumises par les utilisateurs avec les modèles de base de données.

- **`CompteForm`** : Ce formulaire est basé sur le modèle `Compte`. Il permet de créer ou de modifier un compte. 
  - *Personnalisation* : Il utilise un widget spécifique `forms.PasswordInput` pour le champ `mot_de_passe` afin de s'assurer que les caractères saisis sont masqués à l'écran. 
  - *Validation croisée* : Ce formulaire est conçu pour être utilisé potentiellement conjointement avec un formulaire de création d'utilisateur Django natif, afin de garantir que l'objet `User` et l'objet `Compte` soient créés en synchronisation.

## 3. Vues (`views.py`)

Les vues traitent les requêtes HTTP, appliquent la logique métier et renvoient des réponses (généralement via des templates).

- **`compte_list`** : Récupère la liste de tous les comptes pour affichage. Elle utilise `select_related('utilisateur')` pour optimiser les requêtes SQL et éviter le problème du "N+1 query" lors de l'accès aux données de l'utilisateur lié.
- **`compte_create` & `utilisateur_compte_create`** : Gèrent la création de nouveaux comptes. La vue `utilisateur_compte_create` gère la création simultanée d'un utilisateur Django (`User`) et de son `Compte` associé dans une transaction atomique (`@transaction.atomic`), ce qui garantit que si une création échoue, l'autre est annulée, préservant ainsi l'intégrité de la base de données.
- **`compte_update`** : Permet la modification d'un compte existant, en récupérant l'instance via `get_object_or_404` pour une gestion robuste des erreurs 404.
- **`compte_delete`** : Gère la suppression sécurisée d'un compte (souvent via une méthode POST pour respecter les standards de sécurité web contre les attaques CSRF).

## Résumé
L'application `account_management` est conçue pour être robuste, sécurisée (hachage des mots de passe, requêtes atomiques) et optimisée (requêtes jointes). Elle vient compléter le système d'authentification natif de Django avec des règles métier strictes.
