from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    # Obtenez le timestamp actuel
    current_time = timezone.now()

    # Filtrer les notifications envoyées après 10 secondes
    notifications = Notification.objects.filter(user=request.user, timestamp__lte=current_time - timezone.timedelta(seconds=10)).order_by('-timestamp')

    # Organiser les notifications
    notifications_data = [{
        'id': notification.id,
        'message': notification.message,
        'timestamp': notification.timestamp,
        'read': notification.read
    } for notification in notifications]
    
    return Response({'notifications': notifications_data})
