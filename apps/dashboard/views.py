from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from apps.core.mixins import AdminRequiredMixin
from apps.core.choices import PaymentStatus, OrderStatus, NotificationType
from apps.customers.models import CustomerProfile
from apps.menu.models import Food, FoodCategory
from apps.menu.forms import FoodForm
from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService
from apps.payments.models import Payment
from apps.payments.services import PaymentService
from apps.notifications.models import Notification
from apps.notifications.services import NotificationService
from django.core.cache import cache
from apps.core.models import SiteConfiguration
from django.contrib.auth.models import User
from django import forms
from .forms import SiteSettingsForm
from django.db.models import Count, Sum


# ── Forms ─────────────────────────────────────────────────────────────────────

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'address', 'phone_number']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Main Course, Desserts, Beverages',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. main-course, desserts, beverages',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Briefly describe what this category includes...',
            }),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['customer', 'title', 'message', 'notification_type']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = CustomerProfile.objects.all().order_by('full_name')
        self.fields['notification_type'].choices = [
            (NotificationType.MANUAL, NotificationType.MANUAL.label),
        ] + [
            (t.value, t.label) for t in NotificationType
            if t != NotificationType.MANUAL
        ]


# ── Dashboard ─────────────────────────────────────────────────────────────────

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_foods'] = Food.objects.count()
        context['total_customers'] = CustomerProfile.objects.count()
        context['total_orders'] = Order.objects.count()
        context['pending_payments'] = Payment.objects.filter(status=PaymentStatus.PENDING).count()
        context['recent_orders'] = Order.objects.select_related('customer').order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.select_related('customer', 'order').order_by('-created_at')[:5]
        context['page_title'] = 'Admin Dashboard'
        return context


# ── Food Management ───────────────────────────────────────────────────────────

class FoodManagementView(AdminRequiredMixin, ListView):
    model = Food
    template_name = 'admin/foods/index.html'
    context_object_name = 'foods'
    paginate_by = 10

    def get_queryset(self):
        qs = Food.objects.select_related('category').all()
        query = self.request.GET.get('query', '')
        if query:
            qs = qs.filter(name__icontains=query)
        category = self.request.GET.get('category', '')
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoodCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('query', '')
        context['page_title'] = 'Food Management'
        return context


class FoodCreateView(AdminRequiredMixin, CreateView):
    model = Food
    form_class = FoodForm
    template_name = 'admin/foods/create.html'
    success_url = reverse_lazy('dashboard:foods')

    def form_valid(self, form):
        messages.success(self.request, 'Food item created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Food'
        return context


class FoodUpdateView(AdminRequiredMixin, UpdateView):
    model = Food
    form_class = FoodForm
    template_name = 'admin/foods/edit.html'
    success_url = reverse_lazy('dashboard:foods')

    def form_valid(self, form):
        messages.success(self.request, 'Food item updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Food'
        return context


class FoodDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        food = get_object_or_404(Food, pk=pk)
        food.delete()
        messages.success(request, 'Food item deleted.')
        return redirect('dashboard:foods')


# ── Food Category CRUD ────────────────────────────────────────────────────────

class CategoryManagementView(AdminRequiredMixin, ListView):
    model = FoodCategory
    template_name = 'admin/categories/index.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Category Management'
        return context


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = FoodCategory
    form_class = FoodCategoryForm
    template_name = 'admin/categories/create.html'
    success_url = reverse_lazy('dashboard:categories')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Category'
        return context


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = FoodCategory
    form_class = FoodCategoryForm
    template_name = 'admin/categories/edit.html'
    success_url = reverse_lazy('dashboard:categories')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Category'
        return context


class CategoryDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(FoodCategory, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('dashboard:categories')


# ── Customer Management ───────────────────────────────────────────────────────

class CustomerManagementView(AdminRequiredMixin, ListView):
    model = CustomerProfile
    template_name = 'admin/customers/index.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        qs = CustomerProfile.objects.all()
        query = self.request.GET.get('query', '')
        if query:
            qs = qs.filter(full_name__icontains=query) | qs.filter(phone_number__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('query', '')
        context['page_title'] = 'Customer Management'
        return context


class CustomerEditView(AdminRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        form = CustomerProfileForm(instance=customer)
        return render(request, 'admin/customers/edit.html', {
            'form': form,
            'customer': customer,
            'page_title': f'Edit {customer.full_name}',
        })

    def post(self, request, pk):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer profile updated successfully.')
            return redirect('dashboard:customers')
        return render(request, 'admin/customers/edit.html', {
            'form': form,
            'customer': customer,
            'page_title': f'Edit {customer.full_name}',
        })


class CustomerDeleteView(AdminRequiredMixin, View):
    """Delete the auth User (cascades to profile) so no orphan accounts remain."""
    def post(self, request, pk):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        user = customer.user
        user.delete()  # cascades to CustomerProfile via OneToOneField
        messages.success(request, 'Customer account deleted.')
        return redirect('dashboard:customers')


# ── Order Management ──────────────────────────────────────────────────────────

class OrderManagementView(AdminRequiredMixin, ListView):
    model = Order
    template_name = 'admin/orders/index.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        qs = Order.objects.select_related('customer').prefetch_related('items__food').all()
        query = self.request.GET.get('query', '')
        if query:
            qs = qs.filter(order_number__icontains=query) | qs.filter(customer__full_name__icontains=query)
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = OrderStatus.choices
        context['selected_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('query', '')
        context['page_title'] = 'Order Management'
        return context


class OrderStatusUpdateView(AdminRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')

        # No-op check: skip update and notification if status unchanged
        if new_status == order.status:
            messages.info(request, 'Order status is already set to that value.')
            return redirect('dashboard:orders')

        if OrderService.update_status(order, new_status):
            # Only create notification for valid status transitions
            _STATUS_NOTIFICATION_TYPE = {
                OrderStatus.PREPARING: f'order_{OrderStatus.PREPARING}',
                OrderStatus.READY: f'order_{OrderStatus.READY}',
                OrderStatus.DELIVERED: f'order_{OrderStatus.DELIVERED}',
                OrderStatus.CANCELLED: f'order_{OrderStatus.CANCELLED}',
            }
            notif_type = _STATUS_NOTIFICATION_TYPE.get(new_status)
            if notif_type:
                NotificationService.create_notification(
                    customer=order.customer,
                    title=f'Order {order.order_number} Updated',
                    message=f'Your order status has been updated to {order.get_status_display()}.',
                    notification_type=notif_type,
                )
            messages.success(request, 'Order status updated.')
        else:
            messages.error(request, 'Invalid status.')
        return redirect('dashboard:orders')


# ── Payment Verification ──────────────────────────────────────────────────────

class PaymentVerificationView(AdminRequiredMixin, ListView):
    model = Payment
    template_name = 'admin/payments/verification.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        qs = Payment.objects.select_related('customer', 'order').all()
        status = self.request.GET.get('status', '')
        if status and status != 'all':
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statuses = [('all', 'All')] + list(PaymentStatus.choices)
        context['statuses'] = statuses
        context['selected_status'] = self.request.GET.get('status', 'all')
        context['page_title'] = 'Payment Verification'
        return context


class PaymentApproveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        PaymentService.approve_payment(payment)
        messages.success(request, 'Payment approved.')
        return redirect('dashboard:payments')


class PaymentRejectView(AdminRequiredMixin, View):
    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        PaymentService.reject_payment(payment)
        messages.success(request, 'Payment rejected.')
        return redirect('dashboard:payments')


# ── Notification Management ───────────────────────────────────────────────────

class NotificationManagementView(AdminRequiredMixin, ListView):
    model = Notification
    template_name = 'admin/notifications/index.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.select_related('customer').all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Notification Management'
        return context


class NotificationCreateView(AdminRequiredMixin, View):
    """Admin can manually compose and send a notification to any customer."""

    def get(self, request):
        form = NotificationForm(initial={'notification_type': NotificationType.MANUAL})
        return render(request, 'admin/notifications/create.html', {
            'form': form,
            'page_title': 'Send Notification',
        })

    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification sent successfully.')
            return redirect('dashboard:notifications')
        return render(request, 'admin/notifications/create.html', {
            'form': form,
            'page_title': 'Send Notification',
        })


class NotificationDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        messages.success(request, 'Notification deleted.')
        return redirect('dashboard:notifications')


class SettingsView(AdminRequiredMixin, View):
    template_name = 'admin/settings/index.html'

    def get(self, request):
        config = SiteConfiguration.get_instance()
        form = SiteSettingsForm(instance=config, user=request.user)
        return render(request, self.template_name, {
            'form': form,
            'config': config,
            'page_title': 'Settings',
        })

    def post(self, request):
        config = SiteConfiguration.get_instance()
        form = SiteSettingsForm(
            request.POST, request.FILES,
            instance=config, user=request.user,
        )
        if form.is_valid():
            form.save()
            cache.delete('site_config')
            messages.success(request, 'Settings saved successfully.')
            return redirect('dashboard:settings')
        return render(request, self.template_name, {
            'form': form,
            'config': config,
            'page_title': 'Settings',
        })
