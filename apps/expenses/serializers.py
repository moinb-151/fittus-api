from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from ..users.models import User
from .models import Expense, ExpenseSplit
from ..groups.models import Group, GroupMember

class ExpenseCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True)
    group_id = serializers.UUIDField(required=False)
    split_type = serializers.ChoiceField(choices=Expense.SPLIT_CHOICES)
    splits = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        write_only=True
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
    
    def _get_participants(self, expense, splits):
        user_ids = [split['user_id'] for split in splits]

        if expense.paid_by.id not in user_ids:
            raise serializers.ValidationError('Payer must be included in splits.')
        
        if expense.group:
            group_members = GroupMember.objects.filter(
                group=expense.group,
                user_id__in=user_ids
            ).select_related('user')

            if group_members.count() != len(user_ids):
                raise serializers.ValidationError('All split users must be members of the group.')
                
            return [group_member.user for group_member in group_members]
        
        users = list(User.objects.filter(id__in=user_ids))

        if len(users) != len(user_ids):
            raise serializers.ValidationError('Invalid User(s).')
        
        return users
    
    def _map_users(self, split_map):
        users = User.objects.filter(id__in=split_map.keys())
        return {
            user: split_map[user.id].quantize(Decimal('0.01'))
            for user in users
        }
    
    def _calculate_splits(self, expense, participants, splits):
        if expense.split_type == Expense.SPLIT_EQUAL:
            return self._equal_split(expense.amount, participants)

        if expense.split_type == Expense.SPLIT_EXACT:
            return self._exact_split(expense.amount, splits)

        if expense.split_type == Expense.SPLIT_PERCENT:
            return self._percent_split(expense.amount, splits)

        if expense.split_type == Expense.SPLIT_SHARE:
            return self._share_split(expense.amount, splits)

        raise serializers.ValidationError('Invalid split type.')
    
    def _equal_split(self, amount, participants):
        count = len(participants)
        per_head = (amount / Decimal(count)).quantize(Decimal('0.01'))

        return {user: per_head for user in participants}
    
    def _exact_split(self, amount, splits):
        split_map = {}
        total = Decimal('0.00')

        for split in splits:
            val = Decimal(str(split['amount']))
            split_map[split['user_id']] = val
            total += val

        if total != amount:
            raise serializers.ValidationError(
                'Exact split total must equal expense amount.'
            )
        
        return self._map_users(split_map)

    def _percent_split(self, amount, splits):
        split_map = {}
        percent_sum = Decimal('0')

        for split in splits:
            percent = Decimal(str(split['percent']))
            percent_sum += percent
            split_map[split['user_id']] = (amount * percent / 100)

        if percent_sum != 100:
            raise serializers.ValidationError('Percent split must total 100.')
        
        return self._map_users(split_map)
    
    def _share_split(self, amount, splits):
        total_shares = sum(split['shares'] for split in splits)
        per_share = amount / Decimal(total_shares)

        split_map = {split['user_id']: per_share * split['shares'] for split in splits}

        return self._map_users(split_map)
    
    def create(self, validated_data):
        splits = validated_data.pop('splits')

        with transaction.atomic():
            expense = Expense.objects.create(**validated_data)

            participants = self._get_participants(expense, splits)

            split_map = self._calculate_splits(expense, participants, splits)

            ExpenseSplit.objects.bulk_create([
                ExpenseSplit(
                    expense=expense,
                    user=user,
                    amount=amount
                )
                for user, amount in split_map.items()
            ])

        return expense

class ExpenseReadSerializer(serializers.ModelSerializer):
    splits = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'paid_by', 'group', 'split_type', 'created_at', 'splits']

    def get_splits(self, obj):
        return [
            {
                'user_id': split.user.id,
                'amount': split.amount
            }
            for split in obj.splits.all()
        ]