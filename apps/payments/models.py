from django.db import models
from apps.core.choices import PaymentMethod, PaymentStatus
from apps.orders.models import Order
from apps.customers.models import CustomerProfile


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    mobile_number = models.CharField(max_length=20, blank=True)
    network = models.CharField(max_length=20, blank=True)
    card_holder = models.CharField(max_length=100, blank=True)
    card_number = models.CharField(max_length=4, blank=True, help_text='Last 4 digits only')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.get_method_display()}"
