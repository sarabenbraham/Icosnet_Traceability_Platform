from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.connexion_view, name='login'),
    path('logout/', views.deconnexion_view, name='logout'),
    path('profil/', views.profil_view, name='profil'),
    path('utilisateurs/', views.utilisateurs_liste_view, name='utilisateurs_liste'),
    path('utilisateurs/nouveau/', views.utilisateur_creer_view, name='utilisateur_creer'),
]
