from django.urls import path
from .views import SettlementCreateAPIView, SettlementListView, SettlementListByUserView


urlpatterns = [
    path('create/', SettlementCreateAPIView.as_view(), name='create-settlement'),
    path('list/', SettlementListView.as_view(), name='settlement-list'),
    path('list/<int:user_id>/', SettlementListByUserView.as_view(), name='settlement-list-by-user'),
]