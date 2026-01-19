from django.urls import path
from .views import GroupCreateView, AddMembersView

urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='group-create'),
    path('add-members/<int:group_id>/', AddMembersView.as_view(), name='add-members'),
]