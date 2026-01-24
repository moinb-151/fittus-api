from django.db import models
from ..users.models import User

class Balance(models.Model):
    from_user = models.ForeignKey(User, related_name='balances_owed', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='balances_due', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('from_user', 'to_user')