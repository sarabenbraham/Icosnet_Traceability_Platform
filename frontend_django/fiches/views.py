import json
import urllib.request
import urllib.error
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FicheApplicativeForm

# Backend REST API endpoint for fiches
API_BASE = "http://127.0.0.1:8000/api/fiches"


def _api_get(path=""):
    try:
        url = f"{API_BASE}/{path.lstrip('/')}" if path else f"{API_BASE}/"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[FICHES API GET] Error: {exc}")
        return None


def _api_post(path="", data=None):
    try:
        url = f"{API_BASE}/{path.lstrip('/')}" if path else f"{API_BASE}/"
        body = json.dumps(data or {}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8")
        print(f"[FICHES API POST] HTTPError {exc.code}: {err}")
        return None, err
    except Exception as exc:
        print(f"[FICHES API POST] Error: {exc}")
        return None, str(exc)


def _api_put(path="", data=None):
    try:
        url = f"{API_BASE}/{path.lstrip('/')}" if path else f"{API_BASE}/"
        body = json.dumps(data or {}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8")
        print(f"[FICHES API PUT] HTTPError {exc.code}: {err}")
        return None, err
    except Exception as exc:
        print(f"[FICHES API PUT] Error: {exc}")
        return None, str(exc)


def _api_delete(path=""):
    try:
        url = f"{API_BASE}/{path.lstrip('/')}" if path else f"{API_BASE}/"
        req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="DELETE")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in (200, 204)
    except Exception as exc:
        print(f"[FICHES API DELETE] Error: {exc}")
        return False


def _normalize_fiche(f):
    if not f:
        return f
    domaine_map = {
        "RH": "RH", "COMMERCIAL": "Commercial",
        "TECHNIQUE": "Technique / Telco", "MIDDLEWARE": "Middleware",
        "BI": "Décisionnel",
    }
    criticite_map = {
        "CRITIQUE": "Critique", "MAJEURE": "Majeure", "MINEURE": "Mineure",
    }
    domaine = f.get("domaine_fonctionnel", "")
    if isinstance(domaine, list) and len(domaine) > 0:
        dom_val = domaine[0]
    else:
        dom_val = str(domaine)
    f["domaine_label"] = domaine_map.get(dom_val, dom_val)
    f["domaine_fonctionnel"] = dom_val
    f["criticite_label"] = criticite_map.get(f.get("criticite", ""), f.get("criticite", ""))
    f["ingenieur"] = f.get("ingenieur_nom") or "Ahmed Benali"
    return f


def fiche_liste(request):
    """Liste de toutes les fiches applicatives depuis la base de données."""
    raw_fiches = _api_get() or []
    fiches = [_normalize_fiche(f) for f in raw_fiches]

    query = request.GET.get("q", "").strip()
    filtre_statut = request.GET.get("statut", "").strip()
    filtre_domaine = request.GET.get("domaine", "").strip()

    if query:
        fiches = [
            f for f in fiches
            if query.lower() in f.get("nom_application", "").lower()
            or query.lower() in f.get("code_application", "").lower()
        ]
    if filtre_statut:
        fiches = [f for f in fiches if f.get("statut") == filtre_statut]
    if filtre_domaine:
        fiches = [f for f in fiches if f.get("domaine_fonctionnel") == filtre_domaine]

    return render(
        request,
        "fiches/fiche_liste.html",
        {
            "fiches": fiches,
            "query": query,
            "filtre_statut": filtre_statut,
            "filtre_domaine": filtre_domaine,
            "total": len(fiches),
        },
    )


def fiche_detail(request, pk):
    """Détail complet d'une fiche applicative depuis la BDD."""
    fiche = _normalize_fiche(_api_get(f"{pk}/"))
    if not fiche:
        messages.error(request, "Fiche introuvable.")
        return redirect("fiches:liste")
        
    role = _get_user_role(request.user)
    can_validate_fiche = role in ['INGENIEUR', 'CHEF_DEPARTEMENT', 'DIRECTEUR']
    can_delete_fiche = role == 'DIRECTEUR'

    return render(request, "fiches/fiche_detail.html", {
        "fiche": fiche,
        "can_validate_fiche": can_validate_fiche,
        "can_delete_fiche": can_delete_fiche,
    })


def create_fiche_applicative(request):

    if request.method == "POST":

        form = FicheApplicativeCompleteForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                fiche = form.fiche.save()

                contrat = form.contrat.save(commit=False)
                contrat.fiche = fiche
                contrat.save()

                infrastructure = form.infrastructure.save(commit=False)
                infrastructure.fiche = fiche
                infrastructure.save()

                acces = form.acces.save(commit=False)
                acces.fiche = fiche
                acces.save()

                developpement = form.developpement.save(commit=False)
                developpement.fiche = fiche
                developpement.save()

                module_metier = form.module_metier.save(commit=False)
                module_metier.fiche = fiche
                module_metier.save()

                stockage = form.stockage.save(commit=False)
                stockage.fiche = fiche
                stockage.save()

                integration = form.integration.save(commit=False)
                integration.fiche = fiche
                integration.save()

                flux = form.flux.save(commit=False)
                flux.fiche = fiche
                flux.save()

                sauvegarde = form.sauvegarde.save(commit=False)
                sauvegarde.fiche = fiche
                sauvegarde.save()

                intervention = form.intervention.save(commit=False)
                intervention.fiche = fiche
                intervention.save()

            messages.success(
                request,
                "La fiche applicative a été créée avec succès."
            )

            return redirect(
                "application_sheet:fiche_detail",
                pk=fiche.pk
            )

    else:
        form = FicheApplicativeCompleteForm()

    return render(
        request,
        "application_sheet/fiche_form.html",
        {
            "form": form,
        }
    )

def fiche_modifier(request, pk):
    """Formulaire de modification d'une fiche existante."""
    fiche = _normalize_fiche(_api_get(f"{pk}/"))
    if not fiche:
        messages.error(request, "Fiche introuvable.")
        return redirect("fiches:liste")

    if request.method == "POST":
        form = FicheApplicativeForm(request.POST)
        if form.is_valid():
            payload = {
                "nom_application": form.cleaned_data["nom_application"],
                "code_application": form.cleaned_data["code_application"],
                "domaine_fonctionnel": [form.cleaned_data["domaine_fonctionnel"]],
                "criticite": form.cleaned_data["criticite"],
                "description": form.cleaned_data["description"],
                "statut": form.cleaned_data["statut"],
            }
            result, err = _api_put(f"{pk}/", payload)
            if result:
                messages.success(request, f"La fiche « {result.get('nom_application')} » a été mise à jour.")
                return redirect("fiches:detail", pk=pk)
            else:
                messages.error(request, f"Erreur : {err}")
    else:
        initial = {
            "nom_application": fiche.get("nom_application"),
            "code_application": fiche.get("code_application"),
            "domaine_fonctionnel": fiche.get("domaine_fonctionnel"),
            "criticite": fiche.get("criticite"),
            "description": fiche.get("description"),
            "statut": fiche.get("statut"),
        }
        form = FicheApplicativeForm(initial=initial)

    return render(
        request,
        "fiches/fiche_form.html",
        {
            "form": form,
            "fiche": fiche,
            "titre": f"Modifier — {fiche.get('nom_application')}",
            "sous_titre": "Mise à jour des informations de la fiche applicative",
            "mode": "modifier",
        },
    )


def _get_user_role(user):
    if not user or not user.is_authenticated:
        return 'ANONYMOUS'
    username = user.username.lower()
    if user.is_superuser or username in ['admin', 'directeur']:
        return 'DIRECTEUR'
    elif username in ['chef']:
        return 'CHEF_DEPARTEMENT'
    return 'INGENIEUR'


def fiche_soumettre(request, pk):
    result, err = _api_post(f"{pk}/soumettre/")
    if result:
        messages.success(request, f"La fiche a été soumise pour validation.")
    return redirect("fiches:detail", pk=pk)


def fiche_valider(request, pk):
    role = _get_user_role(request.user)
    if role not in ['INGENIEUR', 'CHEF_DEPARTEMENT', 'DIRECTEUR']:
        messages.error(request, "Permission refusée : Vous n'avez pas le droit de valider une fiche.")
        return redirect("fiches:detail", pk=pk)

    result, err = _api_post(f"{pk}/valider/")
    if result:
        messages.success(request, f"La fiche a été validée avec succès !")
    return redirect("fiches:detail", pk=pk)


def fiche_refuser(request, pk):
    role = _get_user_role(request.user)
    if role not in ['INGENIEUR', 'CHEF_DEPARTEMENT', 'DIRECTEUR']:
        messages.error(request, "Permission refusée : Vous n'avez pas le droit de refuser une fiche.")
        return redirect("fiches:detail", pk=pk)

    result, err = _api_post(f"{pk}/refuser/")
    if result:
        motif = request.POST.get("motif_refus", "")
        messages.warning(request, f"La fiche a été refusée. Motif : {motif}")
    return redirect("fiches:detail", pk=pk)


def fiche_supprimer(request, pk):
    role = _get_user_role(request.user)
    if role != 'DIRECTEUR':
        messages.error(request, "Permission refusée : Seul le Directeur DSI peut supprimer définitivement une fiche applicative.")
        return redirect("fiches:detail", pk=pk)

    fiche = _normalize_fiche(_api_get(f"{pk}/"))
    if not fiche:
        messages.error(request, "Fiche introuvable.")
        return redirect("fiches:liste")

    if request.method == "POST":
        ok = _api_delete(f"{pk}/")
        if ok:
            messages.success(request, f"La fiche a été supprimée.")
        return redirect("fiches:liste")

    return render(request, "fiches/fiche_confirm_delete.html", {"fiche": fiche})

