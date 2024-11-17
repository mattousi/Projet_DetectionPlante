from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Favorite
from history.models import SearchHistory
from rest_framework.exceptions import NotFound

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    """
    Ajoute un favori pour l'utilisateur connecté.
    """
    try:
        history_id = request.data.get('history_id')

        # Vérifier si l'historique existe pour l'utilisateur connecté
        history = SearchHistory.objects.get(id=history_id, user=request.user)

        # Créer ou récupérer un favori pour cet utilisateur et cet historique
        favorite, created = Favorite.objects.get_or_create(user=request.user, history=history)

        if created:
            return Response({"message": "Ajouté aux favoris avec succès."})
        else:
            return Response({"message": "Déjà dans les favoris."}, status=400)
    except SearchHistory.DoesNotExist:
        return Response({"error": "Historique non trouvé ou non autorisé."}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, favorite_id):
    """
    Supprime un favori pour l'utilisateur connecté.
    """
    try:
        # Récupérer le favori pour l'utilisateur connecté
        favorite = Favorite.objects.get(id=favorite_id, user=request.user)

        # Supprimer le favori
        favorite.delete()

        return Response({"message": "Supprimé des favoris avec succès."})
    except Favorite.DoesNotExist:
        return Response({"error": "Favori non trouvé ou non autorisé."}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    """
    Récupère la liste des favoris pour l'utilisateur connecté.
    """
    # Filtrer les favoris associés à l'utilisateur connecté
    favorites = Favorite.objects.filter(user=request.user).select_related('history')

    # Construire une réponse structurée
    favorites_data = [
        {
            'id': favorite.id,
            'history_id': favorite.history.id,
            'predicted_class_name': favorite.history.predicted_class_name,
            'added_at': favorite.added_at
        }
        for favorite in favorites
    ]

    return Response({'favorites': favorites_data})
