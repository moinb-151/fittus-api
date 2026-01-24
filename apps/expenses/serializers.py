from rest_framework import serializers
from .models import Expense, ExpenseSplit
from ..groups.models import Group, GroupMember

class ExpenseCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    group_id = serializers.UUIDField(required=False)
    split_type = serializers.ChoiceField(choices=Expense.SPLIT_CHOICES)
    splits = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate(self, attrs):
        user = self.context['request'].user

        if attrs['amount'] <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        
        group_id = attrs.get('group_id')
        if group_id:
            group = Group.objects.filter(id=attrs['group_id']).first()

            if not group:
                raise serializers.ValidationError('Group not found.')

            is_member = GroupMember.objects.filter(group=group, user=user).exists()

            if not is_member:
                raise serializers.ValidationError('You are not member of this group.')
            
            attrs['group'] = group

        attrs['paid_by'] = user

        return attrs 