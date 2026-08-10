from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.core.mixins import CustomerRequiredMixin
from .models import Notification
from .services import NotificationService


class NotificationListView(CustomerRequiredMixin, ListView):
    model = Notification
    template_name = 'public/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(customer=self.request.user.profile).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Notifications'
        unread_count = self.get_queryset().filter(is_read=False).count()
        context['unread_count'] = unread_count
        context['notification_count'] = unread_count
        
        # Get cart count from session
        cart = self.request.session.get('cart', {})
        # Cart values are stored as integers (quantity), so sum directly
        context['cart_count'] = sum(cart.values())
        # Provide full list for Gmail‑like inbox left pane
        context['notification_list'] = self.get_queryset()
        
        return context

# ---------------------------------------------------------------------------
# Gmail‑like inbox – detail view
# ---------------------------------------------------------------------------
class NotificationDetailView(CustomerRequiredMixin, DetailView):
    model = Notification
    template_name = 'public/notification_detail.html'
    context_object_name = 'notification'

    def get_queryset(self):
        # Restrict to the logged‑in customer
        return Notification.objects.filter(customer=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        # Auto‑mark as read when the detail page is accessed (optional)
        response = super().get(request, *args, **kwargs)
        notif = self.object
        if not notif.is_read:
            NotificationService.mark_as_read(notif)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve cart count for the sidebar (same as list view)
        cart = self.request.session.get('cart', {})
        context['cart_count'] = sum(cart.values())
        # Include notification list for left pane
        context['notification_list'] = Notification.objects.filter(customer=self.request.user.profile).order_by('-created_at')
        # Add the related order (if any) for detailed view
        if self.object.order:
            context['order'] = self.object.order
        return context


def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, customer=request.user.profile)
    NotificationService.mark_as_read(notification)
    messages.success(request, 'Notification marked as read.')
    return redirect('notifications:list')


@require_POST
def mark_all_read(request):
    notifications = Notification.objects.filter(customer=request.user.profile, is_read=False)
    count = notifications.count()
    for notif in notifications:
        NotificationService.mark_as_read(notif)
    messages.success(request, f'{count} notification(s) marked as read.')
    return redirect('notifications:list')


@require_POST
def clear_all_notifications(request):
    """Delete all notifications for the current customer."""
    profile = request.user.profile
    count = Notification.objects.filter(customer=profile).count()
    Notification.objects.filter(customer=profile).delete()
    messages.success(request, f'{count} notification(s) cleared.')
    return redirect('notifications:list')
