from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username}'s profile"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)  # Texte de la recherche
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search by {self.user.username}: {self.query}"
