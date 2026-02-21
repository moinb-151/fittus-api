from rest_framework import serializers
from .models import Group, GroupMember
from ..users.serializers import UserRegistrationSerializer

class GroupSerializer(serializers.ModelSerializer):
    created_by = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'group_type', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        group = Group.objects.create(created_by=user, **validated_data)
        GroupMember.objects.create(group=group, user=user, role=GroupMember.ROLE_ADMIN)
        return group
    
class SimplifiedTransactionSerializer(serializers.Serializer):
    from_user_id = serializers.IntegerField(source="from_user.id")
    to_user_id = serializers.IntegerField(source="to_user.id")
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)