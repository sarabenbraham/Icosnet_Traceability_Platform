from django.urls import path
from . import views

app_name = "helpdesk"

urlpatterns = [
    path("",              views.ticket_list,   name="liste"),
    path("nouveau/",      views.ticket_create, name="create"),
    path("<int:pk>/",     views.ticket_detail, name="detail"),
]
