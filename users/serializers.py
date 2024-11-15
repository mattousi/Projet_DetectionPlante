from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, SearchHistory

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['preferences', 'bio', 'profile_image']

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['query', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # Le profil est inclus et non obligatoire
    search_history = SearchHistorySerializer(many=True, read_only=True, source='searchhistory_set')  # Inclure l'historique

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile', 'search_history']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extraire les données du profil si elles existent
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')

        # Créer l'utilisateur
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Créer ou mettre à jour le profil
        Profile.objects.create(user=user, **profile_data)

        return user
