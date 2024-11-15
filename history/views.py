from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import SearchHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_history(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
    print(f"Found {history.count()} history records for user {request.user}")
    history_data = [{
        'id': entry.id,
        'predicted_class_name': entry.predicted_class_name,
        'predicted_class_index': entry.predicted_class_index,
        'predictions': entry.predictions,
        'image_url': entry.image_url,
        'timestamp': entry.timestamp
    } for entry in history]
    
    return JsonResponse({'history': history_data})
