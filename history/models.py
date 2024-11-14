from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , related_name='history_searchhistory')  # Optional: link to a registered user
    predicted_class_name = models.CharField(max_length=255)
    predicted_class_index = models.IntegerField()
    predictions = models.JSONField()  # Store prediction probabilities or scores
    image_url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.predicted_class_name} at {self.timestamp}"
