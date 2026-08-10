from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from apps.core.admin_site import CustomAdminSite

urlpatterns = [

    path('admin/', CustomAdminSite(name='custom_admin').urls),
    path('', include('apps.menu.urls')),
    path('', include('apps.authentication.urls')),
    path('', include('apps.orders.urls')),
    path('dashboard/', include('apps.customers.urls')),
    path('payments/', include('apps.payments.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('admin-panel/', include('apps.dashboard.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/public/img/favicon.svg', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
