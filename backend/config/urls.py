from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from apps.dashboard.views import home as dashboard_home


urlpatterns = [
    path("", lambda request: redirect("dashboard")),
    path("admin/", admin.site.urls),

    path(
        "application_sheet/",
        include("apps.application_sheet.urls"),
    ),

    path(
        "account_management/",
        include("apps.account_management.urls"),
    ),

    path(
        "meetings/",
        include("apps.meetings.urls"),
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "helpdesk/",
        include("apps.helpdesk.urls"),
    ),

    path(
        "dashboard/",
        dashboard_home,
        name="dashboard",
    ),
]