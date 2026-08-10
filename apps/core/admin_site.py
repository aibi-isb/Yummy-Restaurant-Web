from django.contrib.admin import AdminSite
from django.conf import settings
from django.utils.translation import gettext_lazy as _

try:
    from .models import SiteConfiguration
except Exception:
    SiteConfiguration = None


class CustomAdminSite(AdminSite):
    """Admin site that uses a configurable header.

    The header defaults to the ``ADMIN_SITE_HEADER`` setting and falls back to a
    ``SiteConfiguration`` instance if one exists. If both are missing the Django
    default is used. Internationalisation is supported via ``gettext_lazy``.
    """

    site_title = _("Site admin")
    index_title = _("Site administration")

    def __init__(self, name='custom_admin'):
        super().__init__(name)
        # Determine header: DB > settings > default
        header = None
        if SiteConfiguration is not None:
            try:
                config = SiteConfiguration.objects.first()
                if config and getattr(config, "admin_site_header", None):
                    header = config.admin_site_header
                
            except Exception:
                # DB not ready (e.g., migrations not applied)
                pass
        if not header:
            header = getattr(settings, "ADMIN_SITE_HEADER", _("Django administration"))
        self.site_header = header
