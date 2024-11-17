# notification/tasks.py

from celery import shared_task
from .models import Notification
from django.contrib.auth.models import User  # Importez le modèle User
from django.utils import timezone
import random  # Pour choisir une consigne aléatoire

# Liste des messages de consignes
plant_instructions = [
    "Arrosez vos plantes tous les jours.",
    "Exposez vos plantes à la lumière indirecte pour de meilleurs résultats.",
    "Assurez-vous que vos plantes ne sont pas trop proches des fenêtres.",
    "Vérifiez que la température de la pièce est entre 18°C et 25°C.",
    "N'oubliez pas de tailler les feuilles mortes pour encourager la croissance.",
    "Ajoutez un peu de compost à vos plantes pour améliorer la fertilité du sol.",
    "Pensez à changer le terreau de vos plantes tous les deux ans.",
    "Vérifiez que vos plantes sont dans un pot avec des trous de drainage.",
    "Si vos plantes sont en pot, pensez à les rempoter lorsque leurs racines prennent trop de place.",
    "Assurez-vous que vos plantes ne reçoivent pas trop d'eau pour éviter la pourriture des racines.",
    "Gardez vos plantes loin des courants d'air et des changements brusques de température.",
    "En hiver, réduisez l'arrosage de vos plantes, car elles ont besoin de moins d'eau.",
    "Surveillez les feuilles jaunes ou brunes, car cela peut être le signe d'un problème de nutrition ou d'arrosage.",
    "Si vos plantes d'intérieur semblent avoir un peu de mal, essayez de les nettoyer avec un chiffon humide pour éliminer la poussière.",
    "Assurez-vous que vos plantes ont suffisamment d'humidité dans l'air, surtout en hiver.",
    "Changez l'emplacement de vos plantes de temps en temps pour qu'elles bénéficient d'une lumière plus équilibrée."
]

@shared_task
def send_notification():
    """
    Cette tâche envoie une notification à tous les utilisateurs toutes les 10 secondes.
    """
    users = User.objects.all()  # Récupérer tous les utilisateurs
    message = random.choice(plant_instructions)  # Choisir une consigne aléatoire

    for user in users:
        # Créer une notification pour chaque utilisateur
        Notification.objects.create(
            user=user,
            message=message,
            timestamp=timezone.now()
        )
