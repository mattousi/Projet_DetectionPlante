from django.urls import path
from .views import add_favorite, remove_favorite, list_favorites

urlpatterns = [
    path('add/', add_favorite, name='add_favorite'),
    path('remove/<int:favorite_id>/', remove_favorite, name='remove_favorite'),
    path('', list_favorites, name='list_favorites'),
]
