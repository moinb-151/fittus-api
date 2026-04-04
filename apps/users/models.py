from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} ({self.code})"

class User(AbstractUser):
    AUTH_PROVIDER_EMAIL = 'email'
    AUTH_PROVIDER_GOOGLE = 'google'

    AUTH_PROVIDERS = [
        (AUTH_PROVIDER_EMAIL, "Email"),
        (AUTH_PROVIDER_GOOGLE, "Google"),
    ]

    username = None
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    auth_provider = models.CharField(max_length=20, choices=AUTH_PROVIDERS, default=AUTH_PROVIDER_EMAIL)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    default_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Friendship(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    from_user = models.ForeignKey(User, related_name='friendships_initiated', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)