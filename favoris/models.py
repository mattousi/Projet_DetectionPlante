from django.db import models
from django.contrib.auth.models import User
from history.models import SearchHistory  # Assurez-vous que le modèle SearchHistory est correctement importé

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favori de {self.user.username} : {self.history.predicted_class_name}"
