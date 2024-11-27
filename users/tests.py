import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Profile
@pytest.mark.django_db
def test_register_user():
    """
    Test de l'enregistrement d'un nouvel utilisateur.
    """
    client = APIClient()
    url = reverse('register')  # Remplacez 'register' par le nom exact de votre route pour RegisterView

    # Données de test
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }

    # Envoi de la requête POST
    response = client.post(url, user_data, format='json')
    print(User.objects.all()) 
    # Vérifications
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert User.objects.filter(username="testuser").exists()

@pytest.mark.django_db
def test_user_serializer_creates_user():
    """
    Test que le UserSerializer crée un utilisateur et un profil associé.
    """
    # Données pour créer un utilisateur
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }

    # Création de l'instance du serializer
    serializer = UserSerializer(data=user_data)
    
    # Vérification que les données sont valides
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
    
    # Sauvegarde de l'utilisateur via le serializer
    user = serializer.save()

    # Vérification que l'utilisateur a bien été créé dans la base de données
    assert User.objects.filter(username="testuser").exists()

    # Vérification que le profil associé a été créé
    assert Profile.objects.filter(user=user).exists()

    # Vérification que le mot de passe est bien haché (pas stocké en texte clair)
    assert user.password != "strongpassword123"
    assert user.check_password("strongpassword123")  # Vérification du mot de passe haché
