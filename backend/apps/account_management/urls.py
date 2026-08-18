from django.urls import path

from . import views


app_name = "account_management"


urlpatterns = [
    path("", views.compte_list, name="liste"),
    path("create/", views.compte_create, name="create"),
    path("users/create/",views.utilisateur_compte_create,name="utilisateur_compte_create"),
    path("<int:pk>/", views.compte_detail, name="detail"),
    path("<int:pk>/edit/", views.compte_update, name="update"),
    path("<int:pk>/delete/", views.compte_delete, name="delete"),
]