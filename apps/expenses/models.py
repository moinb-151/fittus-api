from django.db import models
from ..users.models import User
from ..groups.models import Group 


class Expense(models.Model):
    SPLIT_EQUAL = 'equal'
    SPLIT_EXACT = 'exact'
    SPLIT_PERCENT = 'percent'
    SPLIT_SHARE = 'share'

    SPLIT_CHOICES = [
        (SPLIT_EQUAL, 'Equal'),
        (SPLIT_EXACT, 'Exact'),
        (SPLIT_PERCENT, 'Percent'),
        (SPLIT_SHARE, 'Share')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES, default=SPLIT_EQUAL)
    paid_by = models.ForeignKey(User, related_name='expenses_paid', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='expenses', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, related_name='splits', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)