from django.db.models import Sum
from django.core.cache import cache
from apps.core.constants import CURRENCY_SYMBOL


def cart_count(request):
    cart = request.session.get('cart', {})
    total = sum(qty for qty in cart.values()) if cart else 0
    return {'cart_count': total}


def notification_count(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        from apps.notifications.models import Notification
        count = Notification.objects.filter(customer=request.user.profile, is_read=False).count()
        return {'notification_count': count}
    return {'notification_count': 0}


def site_config(request):
    config = cache.get('site_config')
    if config is None:
        from apps.core.models import SiteConfiguration
        config = SiteConfiguration.get_instance()
        cache.set('site_config', config, 300)
    return {'site_config': config, 'currency_symbol': CURRENCY_SYMBOL}
