from .models import Notification


class NotificationService:
    @staticmethod
    def create_notification(customer, title, message, notification_type, sender='', order=None):
        return Notification.objects.create(
            customer=customer,
            title=title,
            message=message,
            notification_type=notification_type,
            sender=sender,
            order=order,
        )

    @staticmethod
    def get_unread_count(customer):
        return Notification.objects.filter(customer=customer, is_read=False).count()

    @staticmethod
    def mark_as_read(notification):
        notification.is_read = True
        notification.save(update_fields=['is_read'])
