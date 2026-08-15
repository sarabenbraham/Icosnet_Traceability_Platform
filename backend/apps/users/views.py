from rest_framework import viewsets
from .models import User, Ingenieur, ChefDepartement, Directeur
from .serializers import (
    UserSerializer,
    IngenieurSerializer,
    ChefDepartementSerializer,
    DirecteurSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IngenieurViewSet(viewsets.ModelViewSet):
    queryset = Ingenieur.objects.all()
    serializer_class = IngenieurSerializer


class ChefDepartementViewSet(viewsets.ModelViewSet):
    queryset = ChefDepartement.objects.all()
    serializer_class = ChefDepartementSerializer


class DirecteurViewSet(viewsets.ModelViewSet):
    queryset = Directeur.objects.all()
    serializer_class = DirecteurSerializer
