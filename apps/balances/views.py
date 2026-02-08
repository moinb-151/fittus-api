from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Balance


class BalanceListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        you_owe_qs = Balance.objects.filter(from_user=user).select_related('from_user', 'to_user')
        owed_to_you_qs = Balance.objects.filter(to_user=user).select_related('from_user', 'to_user')

        you_owe = [
            {"user_id": b.to_user_id, "amount": b.amount}
            for b in you_owe_qs
        ]

        you_are_owed = [
            {"user_id": b.from_user_id, "amount": b.amount}
            for b in owed_to_you_qs
        ]

        return Response({
            "you_owe": you_owe,
            "you_are_owed": you_are_owed
        }, status=status.HTTP_200_OK)