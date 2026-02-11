from django.db import models
from ..users.models import User

class Settlement(models.Model):
    payer = models.ForeignKey(User, related_name='settlements_paid', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='settlements_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)