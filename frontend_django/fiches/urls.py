from django.urls import path
from . import views

app_name = 'fiches'

urlpatterns = [
    path('', views.fiche_liste, name='liste'),
    path('nouvelle/', views.fiche_creer, name='creer'),
    path('<int:pk>/', views.fiche_detail, name='detail'),
    path('<int:pk>/modifier/', views.fiche_modifier, name='modifier'),
]
