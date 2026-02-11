from django.db import transaction
from decimal import Decimal
from ..models import Balance


def add_debt(debtor, creditor, amount: Decimal):
    
    if amount <= 0:
        return
    
    balance = Balance.objects.filter(
        from_user=debtor,
        to_user=creditor
    ).first()

    if balance:
        balance.amount += amount
        balance.save()
        return
    
    reverse_balance = Balance.objects.filter(
        from_user=creditor,
        to_user=debtor
    ).first()

    if reverse_balance:
        if reverse_balance.amount > amount:
            reverse_balance.amount -= amount
            reverse_balance.save()
        elif reverse_balance.amount < amount:
            Balance.objects.create(
                from_user=debtor,
                to_user=creditor,
                amount=amount - reverse_balance.amount
            )
            reverse_balance.delete()
        else:
            reverse_balance.delete()

        return
    
    Balance.objects.create(
        from_user=debtor,
        to_user=creditor,
        amount=amount
    )

def reduce_debt(debtor, creditor, amount):
    with transaction.atomic():
        balance = Balance.objects.select_for_update().get(
            from_user=debtor,
            to_user=creditor
        )

        if amount < balance.amount:
            balance.amount -= amount
            balance.save()
        else:
            balance.delete()