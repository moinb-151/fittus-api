from collections import defaultdict
from decimal import Decimal


def simplify_balances(balances):
    net = defaultdict(Decimal)

    for balance in balances:
        net[balance['from_user']] -= balance['amount']
        net[balance['to_user']] += balance['amount']

    
    debtors = []
    creditors = []

    for user, amount in net.items():
        if amount < 0:
            debtors.append([user, amount])
        elif amount > 0:
            creditors.append([user, amount])


    debtors.sort(key=lambda x: x[1])
    creditors.sort(key=lambda x: -x[1])

    transactions = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]

        settle_amount = min(-debt_amount, credit_amount)

        transactions.append({
            'from_user': debtor,
            'to_user': creditor,
            'amount': settle_amount
        })

        debtors[i][1] += settle_amount
        creditors[j][1] -= settle_amount

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transactions