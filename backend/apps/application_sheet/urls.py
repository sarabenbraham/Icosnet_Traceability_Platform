from django.urls import path

from . import views

app_name = "application_sheet"

urlpatterns = [
    path(
        "",
        views.fiche_list,
        name="fiche_list",
    ),

    path(
        "create/",
        views.create_fiche_applicative,
        name="fiche_create",
    ),

    path(
        "<int:pk>/",
        views.fiche_detail,
        name="fiche_detail",
    ),

    path(
        "<int:pk>/delete/",
        views.fiche_delete,
        name="fiche_delete",
    ),
]