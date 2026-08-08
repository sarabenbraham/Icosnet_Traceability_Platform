from django.urls import path

from . import views

app_name = "application_sheet"

urlpatterns = [
    path(
        "create/",
        views.create_fiche_applicative,
        name="fiche_create",
    ),
]