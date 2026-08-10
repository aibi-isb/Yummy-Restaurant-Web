from django.db import models
from django.contrib.auth.models import User


def customer_avatar_upload_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    return f'avatars/user_{instance.user.id}.{ext}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(
        upload_to=customer_avatar_upload_to,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name or self.user.username
