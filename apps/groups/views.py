from django.shortcuts import render
from django.db import transaction
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, GroupMember
from ..users.models import User, Friendship
from .serializers import GroupSerializer


class GroupCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GroupSerializer

class AddMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        user = request.user
        member_ids = request.data.get("member_ids")

        if not isinstance(member_ids, list) or not member_ids:
            return Response(
                {"error": "member_ids must be a non-empty list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response(
                {"error": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        is_admin = GroupMember.objects.filter(
            group=group,
            user=user,
            role=GroupMember.ROLE_ADMIN
        ).exists()

        if not is_admin:
            return Response(
                {"error": "Only group admins can add members"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        existing_member_ids = set(
            GroupMember.objects.filter(group=group)
            .values_list("user_id", flat=True)
        )

        friend_ids = set(
            Friendship.objects.filter(
                status=Friendship.STATUS_ACCEPTED
            ).filter(
                from_user=user
            ).values_list("to_user__id", flat=True)
        ) | set(
            Friendship.objects.filter(
                status=Friendship.STATUS_ACCEPTED
            ).filter(
                to_user=user
            ).values_list("from_user__id", flat=True)
        )

        added = []
        already_members = []
        not_friends = []
        not_found = []

        users_map = {
            u.id: u for u in User.objects.filter(id__in=member_ids)
        }

        with transaction.atomic():
            for member_id in member_ids:

                if member_id == user.id:
                    continue

                member = users_map.get(member_id)

                if not member:
                    not_found.append(member_id)
                    continue

                if member_id in existing_member_ids:
                    already_members.append(member_id)
                    continue

                if member_id not in friend_ids:
                    not_friends.append(member_id)
                    continue

                GroupMember.objects.create(
                    group=group,
                    user=member,
                    role=GroupMember.ROLE_MEMBER
                )
                added.append(member_id)

        
        return Response(
            {
                "added": added,
                "already_members": already_members,
                "not_friends": not_friends,
                "not_found": not_found
            },
            status=status.HTTP_200_OK
        )
    