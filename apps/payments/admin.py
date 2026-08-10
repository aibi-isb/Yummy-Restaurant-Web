from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'amount', 'status', 'created_at']
    list_filter = ['method', 'status']
    search_fields = ['order__order_number', 'customer__full_name']
