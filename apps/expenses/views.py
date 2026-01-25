from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import ExpenseCreateSerializer, ExpenseReadSerializer


class ExpenseCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        expense = serializer.save()

        read_serializer = ExpenseReadSerializer(expense)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)