# model_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_image, name='predict_image'),
]
