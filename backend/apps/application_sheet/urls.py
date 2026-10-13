from django.urls import path

from . import views, workflow

app_name = "application_sheet"

urlpatterns = [
    path("", views.fiche_list, name="liste"),
    path("creer/", views.create_fiche_applicative, name="creer"),
    path("<int:pk>/", views.fiche_detail, name="detail"),
    path("<int:pk>/update/", views.fiche_update, name="modifier"),
    path("<int:pk>/delete/", views.fiche_delete, name="supprimer"),

    # Workflow de validation
    path("<int:pk>/soumettre/", workflow.fiche_soumettre, name="soumettre"),
    path("<int:pk>/valider-chef/", workflow.fiche_valider_chef, name="valider_chef"),
    path("<int:pk>/valider-directeur/", workflow.fiche_valider_directeur, name="valider_directeur"),
    path("<int:pk>/refuser/", workflow.fiche_refuser, name="refuser"),
]