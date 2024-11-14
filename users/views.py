# users/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .serializers import ProfileSerializer, SearchHistorySerializer
from .models import Profile, SearchHistory

# Vue pour l'inscription
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

# Vue pour la déconnexion
from rest_framework.views import APIView

class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Erreur lors de la déconnexion"}, status=status.HTTP_400_BAD_REQUEST)
# Vue pour afficher et mettre à jour le profil de l'utilisateur
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        # Retourne le profil de l'utilisateur connecté
        return Profile.objects.get(user=self.request.user)

# Vue pour créer une nouvelle entrée dans l'historique de recherche
class SearchHistoryCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        query = request.data.get("query")
        if query:
            search_entry = SearchHistory.objects.create(user=request.user, query=query)
            serializer = SearchHistorySerializer(search_entry)
            return Response(serializer.data)
        return Response({"error": "Query not provided"}, status=400)

# Vue pour afficher l'historique de recherche de l'utilisateur
class SearchHistoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        # Retourne l'historique de recherche de l'utilisateur connecté
        return SearchHistory.objects.filter(user=self.request.user).order_by('-timestamp')