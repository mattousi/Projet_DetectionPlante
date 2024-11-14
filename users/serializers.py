# users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, SearchHistory

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['preferences', 'bio', 'profile_image']

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['query', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Inclure le profil dans l'utilisateur
    search_history = SearchHistorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'search_history']
