from rest_framework import generics, permissions
from .models import Settlement
from .serializers import SettlementCreateSerializer


class SettlementCreateAPIView(generics.CreateAPIView):
    queryset = Settlement.objects.all()
    serializer_class = SettlementCreateSerializer
    permission_classes = [permissions.IsAuthenticated]