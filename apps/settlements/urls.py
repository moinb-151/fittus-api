from django.urls import path
from .views import SettlementCreateAPIView


urlpatterns = [
    path('create/', SettlementCreateAPIView.as_view(), name='create-settlement'),
]