from django.urls import path

from . import views


app_name = "account_management"


urlpatterns = [
    path("", views.compte_list, name="liste"),
    path("login/", views.compte_login, name="login"),
    path("logout/", views.compte_logout, name="logout"),
    path("profil/", views.mon_profil, name="profil"),
    path("create/", views.compte_create, name="create"),
    path("<int:pk>/detail/", views.compte_detail, name="detail"),
    path("<int:pk>/update/", views.compte_update, name="update"),
    path("<int:pk>/archiver/", views.compte_archiver, name="archiver"),
    path("archives/", views.comptes_archives, name="archives"),
    path("autocomplete/", views.compte_autocomplete, name="autocomplete"),
]