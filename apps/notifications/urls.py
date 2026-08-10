from django.urls import path
from .views import NotificationListView, NotificationDetailView, mark_notification_read, mark_all_read, clear_all_notifications

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='detail'),
    path('<int:pk>/read/', mark_notification_read, name='mark_read'),
    path('mark-all-read/', mark_all_read, name='mark_all_read'),
    path('clear-all/', clear_all_notifications, name='clear_all'),
]
