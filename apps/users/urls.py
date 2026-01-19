from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, UserProfileView, FriendshipRequestView, FriendshipRequestListView, FriendshipRequestAcceptView, FriendshipRequestRejectView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('friend-request/<int:user_id>/', FriendshipRequestView.as_view(), name='friend-request'),
    path('friend-requests/', FriendshipRequestListView.as_view(), name='friend-request-list'),
    path('friend-request/accept/<int:friendship_id>/', FriendshipRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friend-request/reject/<int:friendship_id>/', FriendshipRequestRejectView.as_view(), name='friend-request-reject'),
]