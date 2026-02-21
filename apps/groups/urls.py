from django.urls import path
from .views import GroupCreateView, AddMembersView, GroupSimplifyView

urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='group-create'),
    path('add-members/<int:group_id>/', AddMembersView.as_view(), name='add-members'),
    path('simplify/<int:group_id>/', GroupSimplifyView.as_view(), name='group-simplify'),
]