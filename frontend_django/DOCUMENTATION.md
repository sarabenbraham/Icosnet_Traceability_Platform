# 📘 Guide & Documentation du Frontend — Plateforme DSI ICOSNET

---

## 🎯 Objectif de l'application

Au sein de la DSI (Direction des Systèmes d'Information) d'ICOSNET, l'objectif est d'avoir une application interne claire pour suivre tout notre parc informatique : fiches applicatives, serveurs, contrats, droits d'accès, sauvegardes et historique des interventions.

Pour construire l'application, le travail a été séparé :
- **Le Backend** : Développé par Sara sous forme d'API REST Django (`Icosnet_Traceability_Platform/backend`).
- **Le Frontend (ce projet)** : Toute la partie visuelle réalisée en **Django MVT (Model-View-Template)**, construite en suivant au pixel près le Design System du Starter Kit officiel **`icoDoc`**.

---

## 💡 Pourquoi l'architecture Django MVT ?

Plutôt que de partir sur un framework React ou Vue complexe, nous avons respecté la consigne du Starter Kit en utilisant **Django MVT**. Les pages sont générées directement côté serveur, ce qui rend l'application ultra rapide à charger, légère et très simple à prendre en main.

Voici comment le code s'articule :
1. **Modèles & Formulaires (`models.py`, `forms.py`)** : Définissent les champs à remplir (nom, code, statut, domaine, criticité) et valident les données saisies.
2. **Les Vues (`views.py`)** : Le cœur de la logique. Elles reçoivent les clics de l'utilisateur, gèrent les recherches et les filtres, et envoient les bonnes infos aux templates.
3. **Les Templates (`templates/`)** : Les fichiers HTML affichés à l'écran, tous basés sur une mise en page commune (`base.html`).

---

## 🎨 Le Style & l'Expérience Visuelle (`icoDoc`)

L'interface a été conçue pour offrir un aspect moderne et épuré (style SaaS pro) :

- **Couleurs principales** :
  - Bleu dynamique : `#2d5be3`
  - Bleu nuit : `#0f1e45` / `#1e3f8a`
  - Fond d'écran : un gris-bleu très doux (`#f0f4fb`) pour éviter la fatigue visuelle.
- **Police d'écriture (Google Fonts)** :
  - **Quicksand** pour les titres, le logo et les gros chiffres du tableau de bord.
  - **Poppins** pour le texte principal, les tableaux et les formulaires.
- **Petits détails qui font la différence** :
  - **Effet Constellation** : Un petit réseau d'étoiles interactif (Canvas HTML5/JS) dans le menu de gauche et la bannière d'accueil.
  - **Icônes fluides** : Directement intégrées en SVG (aucun fichier lourd à charger).
  - **Tailwind CSS** pour la rapidité d'intégration, complété par du CSS sur-mesure.

---

## 📂 Comment sont organisés les fichiers ?

Rien de compliqué, tout est rangé proprement dans le dossier `stage_front` :

```text
stage_front/
├── manage.py                  # Le script officiel pour démarrer le serveur Django
├── DOCUMENTATION.md           # Ce guide
├── templates/                 # Toutes nos pages HTML
│   ├── base.html              # Le squelette commun (menu latéral, topbar, modales)
│   ├── dashboard/
│   │   └── home.html          # Le tableau de bord avec les statistiques
│   └── fiches/
│       ├── fiche_liste.html   # La liste des fiches (avec recherche et filtres)
│       ├── fiche_detail.html  # La vue complète d'une application
│       └── fiche_form.html    # Le formulaire (création & édition)
├── dashboard/                 # L'application Django gérant le tableau de bord
├── fiches/                    # L'application Django gérant les fiches applicatives
└── plateforme_dsi/            # La configuration générale (settings.py, urls.py)
```

---

## 🖥️ Un coup d'œil sur les pages créées

1. **Tableau de bord (`/`)** :
   - Grande bannière de bienvenue avec l'effet constellation.
   - 4 cartes avec les chiffres clés (*Total des fiches, Validées, En attente, Brouillons*).
   - Tableau des dernières activités et répartition par domaine (*RH, Commercial, Telco, Middleware, BI*).

2. **Liste des fiches applicatives (`/fiches/`)** :
   - Barre de recherche instantanée par nom ou code (ex: `ERP-001`).
   - Menus déroulants pour filtrer par statut ou par domaine.
   - Badges de couleurs clairs (*Validée en vert, En attente en orange, Brouillon en gris, Refusée en rouge*).

3. **Détail d'une application (`/fiches/<id>/`)** :
   - Carte d'en-tête avec les badges importants.
   - Vue détaillée sur la description, l'ingénieur responsable et les dates clés.

4. **Formulaire de saisie (`/fiches/nouvelle/`)** :
   - Stepper visuel à 5 étapes (*1. Info générales, 2. Infra, 3. Contrat, 4. Dev, 5. Accès*).
   - Messages d'erreur clairs si un champ obligatoire est manquant.

---

## 🔗 La liaison avec l'API Backend de Sara

Actuellement, l'interface tourne avec des données de démonstration intégrées pour pouvoir tester et valider le visuel immédiatement.

La prochaine étape consistera simplement à relier nos vues Django (`views.py`) aux vrais endpoints de l'API de Sara (`http://127.0.0.1:8000/api/...`) via des requêtes `requests` ou `fetch`.
