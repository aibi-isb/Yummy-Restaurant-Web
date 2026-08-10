from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from decimal import Decimal
from apps.core.mixins import CustomerRequiredMixin, PreventStaffMixin
from apps.core.choices import OrderStatus
from apps.menu.models import Food
from .models import Order
from .forms import CheckoutForm
from .services import OrderService


class CartView(PreventStaffMixin, View):
    template_name = 'public/cart.html'

    TAX_RATE = Decimal('0.005')

    def _build_cart_context(self, cart):
        cart_items = []
        total = Decimal('0.00')
        for food_id, quantity in cart.items():
            food = get_object_or_404(Food, id=food_id)
            subtotal = Decimal(str(quantity)) * food.price
            cart_items.append({'food': food, 'quantity': quantity, 'subtotal': subtotal})
            total += subtotal
        tax = (total * self.TAX_RATE).quantize(Decimal('0.01'))
        grand_total = (total + tax).quantize(Decimal('0.01'))
        return cart_items, total, tax, grand_total

    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items, total, tax, grand_total = self._build_cart_context(cart)
        return render(request, self.template_name, {
            'cart_items': cart_items,
            'total': total,
            'total_with_tax': tax,
            'grand_total': grand_total,
            'page_title': 'Cart',
        })

    def post(self, request):
        food_id = request.POST.get('food_id')
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if action == 'add':
            qty = int(request.POST.get('quantity', 1))
            food_id_str = str(food_id)
            cart[food_id_str] = cart.get(food_id_str, 0) + qty
            messages.success(request, 'Item added to cart.')
        elif action == 'remove':
            cart.pop(str(food_id), None)
            messages.success(request, 'Item removed from cart.')
        elif action == 'update':
            qty = int(request.POST.get('quantity', 1))
            if qty > 0:
                cart[str(food_id)] = qty
            else:
                cart.pop(str(food_id), None)
        elif action == 'clear':
            cart = {}
            messages.success(request, 'Cart cleared.')

        request.session['cart'] = cart
        return redirect('orders:cart')


class CheckoutView(CustomerRequiredMixin, View):
    template_name = 'public/checkout.html'
    TAX_RATE = Decimal('0.005')
    DELIVERY_FEE = Decimal('0.00')

    def _build_cart_summary(self, cart):
        cart_items = []
        subtotal = Decimal('0.00')
        for food_id, quantity in cart.items():
            food = get_object_or_404(Food, id=food_id)
            item_subtotal = Decimal(str(quantity)) * food.price
            cart_items.append({'food': food, 'quantity': quantity, 'subtotal': item_subtotal})
            subtotal += item_subtotal
        tax = (subtotal * self.TAX_RATE).quantize(Decimal('0.01'))
        grand_total = (subtotal + self.DELIVERY_FEE + tax).quantize(Decimal('0.01'))
        return cart_items, subtotal, tax, grand_total

    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, 'Your cart is empty.')
            return redirect('orders:cart')

        cart_items, subtotal, tax, grand_total = self._build_cart_summary(cart)
        profile = request.user.profile
        form = CheckoutForm(initial={
            'street': profile.address,
            'phone': profile.phone_number,
        })
        return render(request, self.template_name, {
            'form': form,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_fee': self.DELIVERY_FEE,
            'tax': tax,
            'grand_total': grand_total,
            'page_title': 'Checkout',
        })

    def post(self, request):
        form = CheckoutForm(request.POST)
        cart = request.session.get('cart', {})

        if not cart:
            messages.warning(request, 'Your cart is empty.')
            return redirect('orders:cart')

        cart_items, subtotal, tax, grand_total = self._build_cart_summary(cart)

        if form.is_valid():
            cart_payload = []
            for food_id, quantity in cart.items():
                food = get_object_or_404(Food, id=food_id)
                cart_payload.append({
                    'food_id': food.id,
                    'quantity': quantity,
                    'price': food.price,
                })

            order = OrderService.create_order(
                customer=request.user.profile,
                cart_items=cart_payload,
                delivery_address=form.delivery_address(),
            )

            request.session['cart'] = {}
            return redirect('payments:checkout', order_id=order.id)

        return render(request, self.template_name, {
            'form': form,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_fee': self.DELIVERY_FEE,
            'tax': tax,
            'grand_total': grand_total,
            'page_title': 'Checkout',
        })


class OrderTrackingView(CustomerRequiredMixin, ListView):
    model = Order
    template_name = 'public/orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    _FILTER_MAP = {
        'preparing': {'status__in': [OrderStatus.PREPARING, OrderStatus.PAYMENT_RECEIVED]},
        'delivered': {'status': OrderStatus.DELIVERED},
        'cancelled': {'status': OrderStatus.CANCELLED},
    }

    def get_queryset(self):
        qs = OrderService.get_customer_orders(self.request.user.profile)
        status = self.request.GET.get('status', '')
        filters = self._FILTER_MAP.get(status)
        if filters:
            qs = qs.filter(**filters)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Orders'
        return context


class OrderDetailView(CustomerRequiredMixin, DetailView):
    model = Order
    template_name = 'public/order_tracking.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.profile).prefetch_related('items__food')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        status = order.status

        steps = [
            {'key': 'received', 'label': 'Received'},
            {'key': 'preparing', 'label': 'Preparing'},
            {'key': 'ready', 'label': 'Ready'},
            {'key': 'in-transit', 'label': 'In Transit'},
            {'key': 'delivered', 'label': 'Delivered'},
        ]
        status_map = {
            OrderStatus.PENDING: 0,
            OrderStatus.PAYMENT_RECEIVED: 0,
            OrderStatus.PREPARING: 1,
            OrderStatus.READY: 2,
            OrderStatus.DELIVERED: 4,
            OrderStatus.CANCELLED: -1,
        }
        current_idx = status_map.get(status, 0)
        progress_steps = []
        for i, step in enumerate(steps):
            if status == OrderStatus.CANCELLED:
                cls = 'completed' if i == 0 else 'cancelled'
            elif i < current_idx:
                cls = 'completed'
            elif i == current_idx:
                cls = 'active'
            else:
                cls = ''
            progress_steps.append({'label': step['label'], 'class': cls})

        timeline_defs = [
            ('received', 'Order Received', OrderStatus.PENDING),
            ('preparing', 'Preparing Food', OrderStatus.PREPARING),
            ('ready', 'Ready for Delivery', OrderStatus.READY),
            ('in-transit', 'In Transit', OrderStatus.READY),
            ('delivered', 'Delivered', OrderStatus.DELIVERED),
        ]
        icons = {
            'received': 'bi-check-circle-fill',
            'preparing': 'bi-gear',
            'ready': 'bi-box-seam',
            'in-transit': 'bi-bicycle',
            'delivered': 'bi-truck',
        }
        order_rank = status_map.get(status, 0)
        timeline = []
        for key, label, threshold_status in timeline_defs:
            threshold = status_map.get(threshold_status, 0)
            completed = order_rank >= threshold and status != OrderStatus.CANCELLED
            item_class = 'completed' if completed else ('active' if order_rank == threshold else '')
            timeline.append({
                'label': label,
                'icon': icons[key],
                'completed': completed,
                'class': item_class,
                'timestamp': order.created_at if completed else None,
            })

        context.update({
            'progress_steps': progress_steps,
            'timeline': timeline,
            'page_title': f'Track Order {order.order_number}',
        })
        return context


@require_POST
def clear_order_history(request):
    """Delete all orders for the current customer."""
    profile = request.user.profile
    count = Order.objects.filter(customer=profile).count()
    Order.objects.filter(customer=profile).delete()
    messages.success(request, f'{count} order(s) cleared from history.')
    return redirect('orders:list')
