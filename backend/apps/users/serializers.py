from rest_framework import serializers
from .models import User, Ingenieur, ChefDepartement, Directeur


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "poste"]


class IngenieurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingenieur
        fields = "__all__"


class ChefDepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefDepartement
        fields = "__all__"


class DirecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directeur
        fields = "__all__"
