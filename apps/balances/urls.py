from django.urls import path
from .views import BalanceListView


urlpatterns = [
    path('list/', BalanceListView.as_view(), name='balance-list'),
]