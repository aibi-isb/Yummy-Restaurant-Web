from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteConfiguration(models.Model):
    """Singleton model to store site‑wide settings."""
    restaurant_name = models.CharField(
        max_length=255,
        default=_('YUMMY Restaurant'),
    )
    admin_site_header = models.CharField(
        max_length=255,
        default=_('Yummy Restaurant Admin'),
        help_text=_('Header displayed on the Django admin site'),
    )
    logo = models.ImageField(
        upload_to='site/',
        blank=True, null=True,
    )
    admin_avatar = models.ImageField(
        upload_to='site/',
        blank=True, null=True,
    )
    payment_received_message = models.TextField(
        default='Payment Verified Successfully. Your order for {{ items }} is now being prepared.',
        help_text='Available variables: {{ customer_name }}, {{ order_number }}, {{ items }}, {{ amount }}',
    )

    class Meta:
        verbose_name = _('site configuration')
        verbose_name_plural = _('site configuration')

    def __str__(self):
        return _('Site Configuration')

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
