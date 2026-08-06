from django.urls import path

from .views import (
    FicheApplicativeListView,
    fiche_create,
    fiche_detail,
    fiche_update,
    FicheApplicativeDeleteView,
)

app_name = "application_sheet"

urlpatterns = [
    path(
        "",
        FicheApplicativeListView.as_view(),
        name="fiche_list",
    ),

    path(
        "create/",
        fiche_create,
        name="fiche_create",
    ),

    path(
        "<int:pk>/",
        fiche_detail,
        name="fiche_detail",
    ),

    path(
        "<int:pk>/edit/",
        fiche_update,
        name="fiche_update",
    ),

    path(
        "<int:pk>/delete/",
        FicheApplicativeDeleteView.as_view(),
        name="fiche_delete",
    ),
]