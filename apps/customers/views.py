from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta, date as date_type
from decimal import Decimal
from apps.core.mixins import CustomerRequiredMixin
from apps.core.choices import OrderStatus, PaymentStatus, NotificationType
from apps.orders.models import Order
from apps.notifications.models import Notification
from .forms import CustomerProfileForm


class CustomerDashboardView(CustomerRequiredMixin, TemplateView):
    template_name = 'public/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.profile
        all_orders = Order.objects.filter(customer=customer)
        orders = all_orders.prefetch_related('items').order_by('-created_at')[:10]
        notifications = Notification.objects.filter(customer=customer).order_by('-created_at')
        in_progress = {OrderStatus.PENDING, OrderStatus.PAYMENT_RECEIVED, OrderStatus.PREPARING, OrderStatus.READY}

        # Flare unread payment-received notifications as Django messages
        unread_received = notifications.filter(
            notification_type=NotificationType.PAYMENT_RECEIVED,
            is_read=False,
        )[:1]
        for note in unread_received:
            messages.success(self.request, note.message)

        # Overall totals
        total_orders = all_orders.count()
        delivered_count = all_orders.filter(status=OrderStatus.DELIVERED).count()
        in_progress_count = all_orders.filter(status__in=in_progress).count()
        total_spent = all_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

        # Trend data: compare last 7 days vs previous 7 days
        today = timezone.now().date()
        last_7 = today - timedelta(days=6)
        prev_14 = today - timedelta(days=14)

        current_period = all_orders.filter(created_at__date__gte=last_7)
        prev_period = all_orders.filter(created_at__date__gte=prev_14, created_at__date__lt=last_7)

        def trend(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return int(round((current - previous) / previous * 100))

        context.update({
            'customer': customer,
            'recent_orders': orders,
            'recent_notifications': notifications[:5],
            'total_orders': total_orders,
            'delivered_count': delivered_count,
            'in_progress_count': in_progress_count,
            'total_spent': total_spent,
            'total_orders_trend': trend(current_period.count(), prev_period.count()),
            'delivered_trend': trend(
                current_period.filter(status=OrderStatus.DELIVERED).count(),
                prev_period.filter(status=OrderStatus.DELIVERED).count(),
            ),
            'in_progress_trend': trend(
                current_period.filter(status__in=in_progress).count(),
                prev_period.filter(status__in=in_progress).count(),
            ),
            'spent_trend': trend(
                current_period.aggregate(total=Sum('total_amount'))['total'] or 0,
                prev_period.aggregate(total=Sum('total_amount'))['total'] or 0,
            ),
            'page_title': 'Dashboard',
        })

        # Chart data: orders & revenue per day (last 7 days)
        chart_data = self._build_chart_data(all_orders, today, last_7)
        context.update(chart_data)
        return context

    def _build_chart_data(self, all_orders, today, start_date):
        dates = []
        d = start_date
        while d <= today:
            dates.append(d)
            d += timedelta(days=1)

        daily = (
            all_orders.filter(created_at__date__gte=start_date)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                count=Count('id'),
                revenue=Sum('total_amount'),
            )
            .order_by('date')
        )
        daily_map = {row['date']: row for row in daily}

        order_counts = []
        revenue_totals = []
        date_labels = []
        for dt in dates:
            date_labels.append(dt.strftime('%b %d'))
            row = daily_map.get(dt)
            order_counts.append(row['count'] if row else 0)
            revenue_totals.append(float(row['revenue']) if row and row['revenue'] else 0)

        return {
            'chart_date_labels': date_labels,
            'chart_order_counts': order_counts,
            'chart_revenue_totals': revenue_totals,
        }


class CustomerProfileView(CustomerRequiredMixin, FormView):
    template_name = 'public/profile.html'
    form_class = CustomerProfileForm
    success_url = '/dashboard/profile/'

    def get_form(self, form_class=None):
        return CustomerProfileForm(instance=self.request.user.profile, **self.get_form_kwargs())

    def form_valid(self, form):
        profile = form.save()
        if self.request.POST.get('avatar_clear'):
            profile.avatar = None
            profile.save()
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.profile
        context.update({
            'customer': customer,
            'total_orders': Order.objects.filter(customer=customer).count(),
            'recent_orders': Order.objects.filter(customer=customer).order_by('-created_at')[:3],
            'recent_notifications': Notification.objects.filter(customer=customer).order_by('-created_at')[:5],
            'page_title': 'My Profile',
            'page_header_title': 'My Profile',
            'page_header_desc': 'Manage your profile information and preferences.',
            'sidebar_account_header': 'Your Account',
            'profile_nav_label': 'Profile',
            'sidebar_section_header_preferences': 'Preferences',
            'profile_section_title': 'Profile',
            'personal_info_desc': 'Your personal information and contact details.',
            'upload_image_label': 'Upload Image',
            'remove_image_label': 'Remove',
            'file_hint': 'PNGs, JPEGs and GIFs under 10MB',
            'full_name_label': 'Full Name',
            'email_description': 'Your email address is used to log in to your account and cannot be changed here.',
            'phone_number_label': 'Phone Number',
            'address_label': 'Address',
            'save_changes_label': 'Save Changes',
            'cancel_label': 'Cancel',
        })
        return context


class CustomerProfileEditView(CustomerRequiredMixin, View):
    def get(self, request):
        return redirect('customers:profile')

    def post(self, request):
        return redirect('customers:profile')
