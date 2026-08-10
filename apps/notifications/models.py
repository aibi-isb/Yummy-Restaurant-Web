from django.db import models
from apps.core.choices import NotificationType
from apps.customers.models import CustomerProfile
from apps.orders.models import Order


class Notification(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='notifications')
    sender = models.CharField(max_length=100, blank=True)  # e.g., restaurant name or system
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NotificationType.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
