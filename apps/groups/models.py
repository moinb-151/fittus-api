from django.db import models
from ..users.models import User


class Group(models.Model):
    TYPE_TRIP = 'trip'
    TYPE_HOME = 'home'
    TYPE_COUPLE = 'couple'
    TYPE_OTHER = 'other'

    TYPE_CHOICES = [
        (TYPE_TRIP, 'Trip'),
        (TYPE_HOME, 'Home'),
        (TYPE_COUPLE, 'Couple'),
        (TYPE_OTHER, 'Other'),
    ]

    name = models.CharField(max_length=100)
    group_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_by = models.ForeignKey(User, related_name='groups_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GroupMember(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MEMBER, 'Member'),
    ]

    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='group_memberships', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')