from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    IngenieurViewSet,
    ChefDepartementViewSet,
    DirecteurViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("ingenieurs", IngenieurViewSet)
router.register("chefs-departement", ChefDepartementViewSet)
router.register("directeurs", DirecteurViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
