ORDER_STATUS_CHOICES = {
    'PENDING': 'pending',
    'PAYMENT_RECEIVED': 'payment_received',
    'PREPARING': 'preparing',
    'READY': 'ready',
    'DELIVERED': 'delivered',
    'CANCELLED': 'cancelled',
}

PAYMENT_STATUS_CHOICES = {
    'PENDING': 'pending',
    'APPROVED': 'approved',
    'REJECTED': 'rejected',
}

PAYMENT_METHOD_CHOICES = {
    'MOBILE_MONEY': 'mobile_money',
    'CARD': 'card',
}

NOTIFICATION_TYPE_CHOICES = {
    'PAYMENT_RECEIVED': 'payment_received',
    'PAYMENT_REJECTED': 'payment_rejected',
    'ORDER_CONFIRMED': 'order_confirmed',
    'ORDER_PREPARING': 'order_preparing',
    'ORDER_READY': 'order_ready',
    'ORDER_DELIVERED': 'order_delivered',
    'MANUAL': 'manual',
}

MAX_CART_ITEMS = 20
DEFAULT_PAGE_SIZE = 12
CURRENCY_SYMBOL = 'Le'
