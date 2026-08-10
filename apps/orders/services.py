from decimal import Decimal
from django.db import transaction
from apps.core.helpers import generate_order_number
from apps.core.choices import OrderStatus
from .models import Order, OrderItem


class OrderService:
    @staticmethod
    def calculate_total(items):
        total = Decimal('0.00')
        for item in items:
            quantity = item.get('quantity', 0)
            price = item.get('price', Decimal('0.00'))
            total += Decimal(str(quantity)) * Decimal(str(price))
        return total

    @staticmethod
    @transaction.atomic
    def create_order(customer, cart_items, delivery_address):
        total = OrderService.calculate_total(cart_items)
        order = Order.objects.create(
            customer=customer,
            order_number=generate_order_number(),
            delivery_address=delivery_address,
            total_amount=total,
            status=OrderStatus.PENDING,
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_id=item['food_id'],
                quantity=item['quantity'],
                unit_price=item['price'],
                subtotal=Decimal(str(item['quantity'])) * Decimal(str(item['price'])),
            )
        return order

    @staticmethod
    def update_status(order, new_status):
        valid_statuses = [s[0] for s in OrderStatus.choices]
        if new_status in valid_statuses:
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            return True
        return False

    @staticmethod
    def get_customer_orders(customer):
        return Order.objects.filter(customer=customer).prefetch_related('items__food').order_by('-created_at')
