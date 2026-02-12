from rest_framework import serializers
from django.db import transaction
from .models import Settlement
from ..balances.models import Balance
from ..users.models import User
from decimal import Decimal
from ..balances.utils.update_balances import reduce_debt


class SettlementCreateSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        receiver_id = attrs.get('receiver_id')
        amount = attrs.get('amount')

        payer = self.context.get('request').user
        receiver = User.objects.filter(id=receiver_id).first()

        if not receiver:
            raise serializers.ValidationError('Receiver does not exist.')
        
        if payer == receiver:
            raise serializers.ValidationError('You cannot settle with yourself.')
        
        balance = Balance.objects.filter(from_user=payer, to_user=receiver).first()

        if not balance:
            raise serializers.ValidationError('No settlement required.')
        
        if amount <= Decimal('0'):
            raise serializers.ValidationError('Amount must be greater than zero.')
        
        if amount > balance.amount:
            raise serializers.ValidationError('Cannot settle more than what you owe.')
        
        attrs["payer"] = payer
        attrs["receiver"] = receiver
        attrs["balance"] = balance
        
        return attrs
        
    def create(self, validated_data):
        payer = validated_data['payer']
        receiver = validated_data['receiver']
        amount = validated_data['amount']

        with transaction.atomic():
            settlement = Settlement.objects.create(
                payer=payer,
                receiver=receiver,
                amount=amount
            )

            reduce_debt(
                debtor=payer,
                creditor=receiver,
                amount=amount
            )

        return settlement

class SettlementListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Settlement
        fields = ["user_id", "amount", "created_at"]

    def get_user_id(self, obj):
        request_user = self.context["request"].user

        if obj.payer == request_user:
            return obj.receiver_id
        return obj.payer_id