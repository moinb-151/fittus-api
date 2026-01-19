from django.shortcuts import render
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import User, Friendship
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, FriendshipSerializer


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRegistrationSerializer
    
    def get_object(self):
        return self.request.user
    
class FriendshipRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if to_user == request.user:
            return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship, created = Friendship.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

        if not created:
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        friendship_data = FriendshipSerializer(friendship).data

        return Response({'message': 'Friend request sent.', 'friendship': friendship_data}, status=status.HTTP_201_CREATED)
    
class FriendshipRequestListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        return Friendship.objects.filter(to_user=self.request.user, status=Friendship.STATUS_PENDING).select_related('from_user', 'to_user')
    
class FriendshipRequestAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, friendship_id):
        try:
            friendship = Friendship.objects.get(id=friendship_id, to_user=request.user)
        except Friendship.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if friendship.status != Friendship.STATUS_PENDING:
            return Response({'error': 'You have already responded to this friend request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = Friendship.STATUS_ACCEPTED
        friendship.save(update_fields=['status'])

        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
    
class FriendshipRequestRejectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, friendship_id):
        try:
            friendship = Friendship.objects.get(id=friendship_id, to_user=request.user)
        except Friendship.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if friendship.status != Friendship.STATUS_PENDING:
            return Response({'error': 'You have already responded to this friend request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = Friendship.STATUS_REJECTED
        friendship.save(update_fields=['status'])

        return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)
    