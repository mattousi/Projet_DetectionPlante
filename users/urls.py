# users/urls.py

from django.urls import path
from .views import  RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileView, SearchHistoryCreateView, SearchHistoryListView
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('search-history/', SearchHistoryListView.as_view(), name='search-history-list'),
    path('search-history/create/', SearchHistoryCreateView.as_view(), name='search-history-create'),
    
]
