# Diagrammes Techniques - Gestion de Comptes

## Diagramme de Classes

```mermaid
classDiagram
    class Compte {
        +OneToOneField utilisateur
        +EmailField email_connexion
        +CharField mot_de_passe
        +DateTimeField date_creation
        +DateField date_expiration
        +CharField statut
        +BooleanField expire
        +set_password(raw_password)
        +check_password(raw_password) bool
        +verifier_expiration() bool
    }

    class AUTH_USER_MODEL {
        <<Django Default User>>
    }

    AUTH_USER_MODEL "1" -- "1" Compte : possède >
```

### Description du Diagramme de Classes

Le système s'articule autour de l'entité `Compte`.

**Relations :**
* Le `Compte` étend le modèle utilisateur par défaut de Django (`AUTH_USER_MODEL`) via une relation **OneToOneField**. Si l'utilisateur principal est supprimé, son profil de connexion l'est aussi (via `on_delete=models.CASCADE`).

**Énumérations (Enums) :**
* **Statut (`Compte.Statut`)** : Les choix possibles sont `ACTIF` ou `DESACTIVE`.

---

## Diagrammes d'Activité et de Séquence

### 1. Workflow : Vérification de l'Expiration du Compte (Activité)

```mermaid
stateDiagram-v2
    [*] --> Verification : Appel de verifier_expiration()
    
    Verification --> Check_Date
    
    state Check_Date {
        Date_Valide : Date actuelle < Date_expiration
        Date_Depassee : Date actuelle >= Date_expiration
    }
    
    Check_Date --> Date_Valide
    Check_Date --> Date_Depassee
    
    Date_Valide --> Compte_Valide : Return False
    
    Date_Depassee --> Check_Statut : Vérifier le statut
    
    Check_Statut --> Statut_Desactive : Statut == DESACTIVE
    Statut_Desactive --> Compte_Valide : Return False
    
    Check_Statut --> Bascule_Expiration : Statut == ACTIF
    Bascule_Expiration --> Update_DB : save(update_fields=["expire"])
    Update_DB --> Compte_Expire : Return True
    
    Compte_Valide --> [*]
    Compte_Expire --> [*]
```

### 2. Séquence : Création / Hashage du Mot de Passe

```mermaid
sequenceDiagram
    participant Application
    participant CompteModel as Modèle Compte
    participant Hasher as django.contrib.auth.hashers

    Application->>CompteModel: set_password("mon_mot_de_passe")
    CompteModel->>Hasher: make_password("mon_mot_de_passe")
    Hasher-->>CompteModel: hash_sécurisé (ex: pbkdf2_sha256$...)
    CompteModel->>CompteModel: self.mot_de_passe = hash_sécurisé
    Application->>CompteModel: save()
```

---

## URLs et Vues

> **Note :** À l'heure actuelle, le module `account_management` encapsule la structure de la base de données et la logique métier de sécurité cryptographique au sein du modèle (`models.py`). 
> 
> Les URLs et les Vues Django associées (endpoints web pour l'interface de connexion, d'inscription ou d'administration personnalisée) sont en cours d'intégration et le fichier `urls.py` n'a pas encore de routes exposées. 
