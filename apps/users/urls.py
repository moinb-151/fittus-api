from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]