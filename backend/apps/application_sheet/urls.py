from django.urls import path

from . import views

app_name = "application_sheet"

urlpatterns = [
    path(
        "",
        views.fiche_list,
        name="liste",
    ),

    path(
        "creer/",
        views.create_fiche_applicative,
        name="creer",
    ),

    path(
        "<int:pk>/",
        views.fiche_detail,
        name="detail",
    ),

    path(
        "<int:pk>/update/",
        views.fiche_update,
        name="modifier",
    ),

    path(
        "<int:pk>/delete/",
        views.fiche_delete,
        name="supprimer",
    ),
]