from django.db import transaction
from django.template import Template, Context
from apps.core.choices import PaymentStatus, NotificationType, OrderStatus, PaymentMethod
from apps.core.models import SiteConfiguration
from .models import Payment
from apps.notifications.services import NotificationService


class PaymentService:
    @staticmethod
    @transaction.atomic
    def process_payment(order, method, data):
        payment_data = {
            'order': order,
            'customer': order.customer,
            'method': method,
            'amount': order.total_amount,
            'status': PaymentStatus.PENDING,
        }
        if method == PaymentMethod.MOBILE_MONEY:
            payment_data['mobile_number'] = data.get('mobile_number', '')
            payment_data['network'] = data.get('network', '')
        elif method == PaymentMethod.CARD:
            payment_data['card_holder'] = data.get('card_holder', '')
            card_number = data.get('card_number', '')
            payment_data['card_number'] = card_number[-4:] if len(card_number) >= 4 else card_number

        return Payment.objects.create(**payment_data)

    @staticmethod
    @transaction.atomic
    def approve_payment(payment):
        payment.status = PaymentStatus.APPROVED
        payment.save(update_fields=['status'])

        payment.order.status = OrderStatus.PAYMENT_RECEIVED
        payment.order.save(update_fields=['status', 'updated_at'])

        items = payment.order.items.select_related('food').all()
        item_names = ', '.join([item.food.name for item in items[:3]])
        if len(items) > 3:
            item_names += f' and {len(items) - 3} more item(s)'

        config = SiteConfiguration.get_instance()
        msg_template = Template(config.payment_received_message)
        message = msg_template.render(Context({
            'customer_name': payment.customer.full_name,
            'order_number': payment.order.order_number,
            'items': item_names,
            'amount': f'Le {payment.amount}',
        }))

        NotificationService.create_notification(
            customer=payment.customer,
            title='Payment Verified Successfully',
            message=message,
            notification_type=NotificationType.PAYMENT_RECEIVED,
            sender='Yummy Restaurant',
            order=payment.order,
        )

    @staticmethod
    @transaction.atomic
    def reject_payment(payment):
        payment.status = PaymentStatus.REJECTED
        payment.save(update_fields=['status'])

        NotificationService.create_notification(
            customer=payment.customer,
            title='Payment Rejected',
            message=f'Your payment of Le {payment.amount} for order {payment.order.order_number} has been rejected.',
            notification_type=NotificationType.PAYMENT_REJECTED,
        )
