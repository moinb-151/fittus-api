from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..users.models import User
from .models import Settlement
from .serializers import SettlementCreateSerializer, SettlementListSerializer


class SettlementCreateAPIView(generics.CreateAPIView):
    queryset = Settlement.objects.all()
    serializer_class = SettlementCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class SettlementListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        paid = user.settlements_paid.select_related('receiver').order_by('-created_at')
        received = user.settlements_received.select_related('payer').order_by('-created_at')

        return Response({
            'paid': SettlementListSerializer(
                paid, many=True, context={'request': request}
            ).data,
            'received': SettlementListSerializer(
                received, many=True, context={'request': request}
            ).data,
        }, status=status.HTTP_200_OK)
    
class SettlementListByUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        
        requested_user = User.objects.filter(id=user_id).first()

        if not requested_user:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        paid = user.settlements_paid.filter(receiver=requested_user).select_related('receiver').order_by('-created_at')
        received = user.settlements_received.filter(payer=requested_user).select_related('payer').order_by('-created_at')

        return Response({
            'paid': SettlementListSerializer(
                paid, many=True, context={'request': request}
            ).data,
            'received': SettlementListSerializer(
                received, many=True, context={'request': request}
            ).data,
        }, status=status.HTTP_200_OK)