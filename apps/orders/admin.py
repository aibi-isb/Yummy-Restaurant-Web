from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['order_number', 'customer', 'total_amount', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['order_number', 'customer__full_name']
