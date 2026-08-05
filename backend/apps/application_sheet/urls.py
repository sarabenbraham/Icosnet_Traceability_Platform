from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()


router.register(
    "fiches",
    FicheApplicativeViewSet
)

router.register(
    "contrats",
    ContratViewSet
)

router.register(
    "infrastructures",
    InfrastructureViewSet
)

router.register(
    "acces",
    UtilisateurAccesViewSet
)

router.register(
    "developpements",
    DeveloppementViewSet
)

router.register(
    "modules",
    ModuleMetierViewSet
)

router.register(
    "stockages",
    StockageViewSet
)

router.register(
    "integrations",
    IntegrationViewSet
)

router.register(
    "flux",
    FluxApplicationViewSet
)

router.register(
    "sauvegardes",
    SauvegardeViewSet
)

router.register(
    "interventions",
    InterventionViewSet
)


urlpatterns = [
    path(
        "",
        include(router.urls)
    )
]

