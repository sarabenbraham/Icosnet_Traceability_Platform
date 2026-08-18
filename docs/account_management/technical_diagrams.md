# Diagrammes Techniques - Gestion de Comptes

*(Les diagrammes de classes, d'activité et de séquence ont été insérés en format image. Vous trouverez ci-dessous les explications détaillant la logique de ces diagrammes pour accompagner les photos).*

## 1. Description du Diagramme de Classes

Le système s'articule autour de l'entité de sécurité `Compte`.

**Relations :**
* L'entité `Compte` étend le modèle utilisateur par défaut de Django (`AUTH_USER_MODEL`) via une relation **OneToOneField**. Si l'utilisateur principal est supprimé, son profil de connexion l'est aussi automatiquement (grâce à `on_delete=models.CASCADE`).

**Champs et Énumérations (Enums) :**
* Le compte possède un identifiant unique de connexion (`email_connexion`) et un `mot_de_passe` sécurisé.
* Les dates permettent de tracer la création (`date_creation`) et la limite de validité (`date_expiration`).
* Le champ `expire` (booléen) indique de manière rapide si le compte a dépassé sa date de validité.
* **Statut (`Compte.Statut`)** : Les choix possibles pour le statut sont strictement limités à `ACTIF` ou `DESACTIVE`.

---

## 2. Diagrammes d'Activité et de Séquence

### A. Workflow : Vérification de l'Expiration du Compte (Activité)

Le diagramme d'activité illustre le comportement de la méthode `verifier_expiration()` :
1. **Vérification de la Date** : Le système compare la date actuelle avec la `date_expiration` définie dans le compte.
2. **Date Valide** : Si la date actuelle est strictement inférieure à la date d'expiration, le processus s'arrête et retourne `False` (le compte n'est pas expiré).
3. **Date Dépassée** : Si la date d'expiration est atteinte ou dépassée, le système vérifie le statut du compte :
   * Si le statut est déjà `DESACTIVE`, il ne se passe rien (la méthode retourne `False`).
   * Si le statut est `ACTIF`, le système bascule le champ `expire` à `True`, effectue une mise à jour uniquement sur ce champ précis dans la base de données (`save(update_fields=["expire"])`), et retourne `True` pour confirmer l'expiration effective.

### B. Séquence : Création et Hachage du Mot de Passe

Le diagramme de séquence décrit le processus de sécurisation d'un mot de passe via la méthode `set_password()` :
1. L'application (ou la vue) transmet le mot de passe en clair à la méthode `set_password("...")` du modèle `Compte`.
2. Le modèle fait appel à la fonction cryptographique `make_password()` issue du module `django.contrib.auth.hashers`.
3. Ce module génère une empreinte sécurisée (hash) à partir du mot de passe (généralement via l'algorithme par défaut pbkdf2_sha256).
4. Le modèle assigne cette empreinte illisible au champ `self.mot_de_passe`.
5. L'application appelle finalement la méthode `save()` pour stocker de façon permanente ce hash sécurisé en base de données. Le mot de passe en clair n'est jamais conservé.

---

## 3. URLs et Vues

> **Note :** À l'heure actuelle, le module `account_management` encapsule la structure de la base de données et la logique métier de sécurité (vérifications, expirations, hachage) directement au sein du modèle (`models.py`). 
> 
> Les URLs et les Vues Django (endpoints web ou API pour les pages de login, d'inscription ou d'administration) sont en cours d'intégration. Le fichier de routage `urls.py` ne contient donc pas encore de chemins exposés pour ce module.
