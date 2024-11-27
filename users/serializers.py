from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Le mot de passe est en écriture seule pour la sécurité
            'email': {'required': True},  # L'email est obligatoire
        }

    def create(self, validated_data):
        # Extraire le mot de passe et créer l'utilisateur
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # Utiliser `create_user` pour la gestion sécurisée
        user.set_password(password)
        user.save()

        # Créer automatiquement le profil associé
        Profile.objects.create(user=user)

        return user
