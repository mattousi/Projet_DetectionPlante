from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_history, name='view_history'),  # API endpoint to view history
]
