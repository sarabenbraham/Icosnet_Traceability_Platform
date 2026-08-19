from django.urls import path

from . import views


app_name = "meetings"


urlpatterns = [

    # =====================================================
    # LIEUX
    # =====================================================

    path(
        "lieux/",
        views.lieu_list,
        name="lieu_list",
    ),

    path(
        "lieux/create/",
        views.lieu_create,
        name="lieu_create",
    ),

    path(
        "lieux/<uuid:pk>/",
        views.lieu_detail,
        name="lieu_detail",
    ),

    path(
        "lieux/<uuid:pk>/edit/",
        views.lieu_update,
        name="lieu_update",
    ),

    path(
        "lieux/<uuid:pk>/delete/",
        views.lieu_delete,
        name="lieu_delete",
    ),

    # =====================================================
    # REUNIONS
    # =====================================================

    path(
        "",
        views.reunion_list,
        name="reunion_list",
    ),

    path(
        "create/",
        views.reunion_create,
        name="reunion_create",
    ),

    path(
        "<uuid:pk>/",
        views.reunion_detail,
        name="reunion_detail",
    ),

    path(
        "<uuid:pk>/edit/",
        views.reunion_update,
        name="reunion_update",
    ),

    path(
        "<uuid:pk>/delete/",
        views.reunion_delete,
        name="reunion_delete",
    ),

    # =====================================================
    # PARTICIPATIONS
    # =====================================================

    path(
        "<uuid:reunion_pk>/participants/create/",
        views.participation_create,
        name="participation_create",
    ),

    path(
        "participations/<uuid:pk>/delete/",
        views.participation_delete,
        name="participation_delete",
    ),

    path(
        "participations/<uuid:pk>/confirm/",
        views.participation_confirmer,
        name="participation_confirmer",
    ),

    path(
        "participations/<uuid:pk>/refuse/",
        views.participation_refuser,
        name="participation_refuser",
    ),
]