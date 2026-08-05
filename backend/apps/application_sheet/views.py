from rest_framework import viewsets

from .models import (
    FicheApplicative,
    Contrat,
    Infrastructure,
    UtilisateurAcces,
    Developpement,
    ModuleMetier,
    Stockage,
    Integration,
    FluxApplication,
    Sauvegarde,
    Intervention,
)

from .serializers import *


class FicheApplicativeViewSet(viewsets.ModelViewSet):

    queryset = FicheApplicative.objects.all()

    serializer_class = FicheApplicativeSerializer



class ContratViewSet(viewsets.ModelViewSet):

    queryset = Contrat.objects.all()

    serializer_class = ContratSerializer



class InfrastructureViewSet(viewsets.ModelViewSet):

    queryset = Infrastructure.objects.all()

    serializer_class = InfrastructureSerializer



class UtilisateurAccesViewSet(viewsets.ModelViewSet):

    queryset = UtilisateurAcces.objects.all()

    serializer_class = UtilisateurAccesSerializer



class DeveloppementViewSet(viewsets.ModelViewSet):

    queryset = Developpement.objects.all()

    serializer_class = DeveloppementSerializer



class ModuleMetierViewSet(viewsets.ModelViewSet):

    queryset = ModuleMetier.objects.all()

    serializer_class = ModuleMetierSerializer



class StockageViewSet(viewsets.ModelViewSet):

    queryset = Stockage.objects.all()

    serializer_class = StockageSerializer



class IntegrationViewSet(viewsets.ModelViewSet):

    queryset = Integration.objects.all()

    serializer_class = IntegrationSerializer



class FluxApplicationViewSet(viewsets.ModelViewSet):

    queryset = FluxApplication.objects.all()

    serializer_class = FluxApplicationSerializer



class SauvegardeViewSet(viewsets.ModelViewSet):

    queryset = Sauvegarde.objects.all()

    serializer_class = SauvegardeSerializer



class InterventionViewSet(viewsets.ModelViewSet):

    queryset = Intervention.objects.all()

    serializer_class = InterventionSerializer