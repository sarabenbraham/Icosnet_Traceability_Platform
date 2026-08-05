from rest_framework import serializers

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


class ContratSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contrat
        fields = "__all__"



class InfrastructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Infrastructure
        fields = "__all__"



class UtilisateurAccesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UtilisateurAcces
        fields = "__all__"



class DeveloppementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developpement
        fields = "__all__"



class ModuleMetierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModuleMetier
        fields = "__all__"



class StockageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stockage
        fields = "__all__"



class IntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Integration
        fields = "__all__"



class FluxApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FluxApplication
        fields = "__all__"



class SauvegardeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sauvegarde
        fields = "__all__"



class InterventionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Intervention
        fields = "__all__"



class FicheApplicativeSerializer(serializers.ModelSerializer):

    contrat = ContratSerializer(read_only=True)
    infrastructure = InfrastructureSerializer(read_only=True)
    utilisateurs_acces = UtilisateurAccesSerializer(read_only=True)
    developpement = DeveloppementSerializer(read_only=True)
    stockage = StockageSerializer(read_only=True)
    integration = IntegrationSerializer(read_only=True)

    modules = ModuleMetierSerializer(
        many=True,
        read_only=True
    )

    flux = FluxApplicationSerializer(
        many=True,
        read_only=True
    )

    interventions = InterventionSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = FicheApplicative

        fields = [
            "id",
            "nom_application",
            "code_application",
            "domaine_fonctionnel",
            "criticite",
            "description",
            "date_creation",
            "statut",
            "ingenieur",
            "departements",

            "contrat",
            "infrastructure",
            "utilisateurs_acces",
            "developpement",
            "stockage",
            "integration",
            "modules",
            "flux",
            "interventions",
        ]