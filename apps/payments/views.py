from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from apps.core.mixins import CustomerRequiredMixin
from apps.core.choices import PaymentMethod
from apps.orders.models import Order
from .forms import MobileMoneyForm, CardForm
from .services import PaymentService


class PaymentView(CustomerRequiredMixin, View):
    template_name = 'public/payment.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user.profile)

        if hasattr(order, 'payment'):
            messages.info(request, 'Payment already submitted for this order.')
            return redirect('orders:list')

        mobile_form = MobileMoneyForm(initial={'amount': order.total_amount})
        card_form = CardForm(initial={'amount': order.total_amount})

        return render(request, self.template_name, {
            'order': order,
            'mobile_form': mobile_form,
            'card_form': card_form,
            'page_title': 'Payment',
        })

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user.profile)

        if hasattr(order, 'payment'):
            messages.warning(request, 'Payment already submitted.')
            return redirect('orders:list')

        method = request.POST.get('payment_method')

        if method == PaymentMethod.MOBILE_MONEY:
            form = MobileMoneyForm(request.POST)
            if form.is_valid():
                PaymentService.process_payment(order, PaymentMethod.MOBILE_MONEY, form.cleaned_data)
                messages.success(request, 'Payment submitted successfully! Awaiting approval.')
                return redirect('payments:success', order_id=order.id)
            mobile_form = form
            card_form = CardForm(initial={'amount': order.total_amount})
        elif method == PaymentMethod.CARD:
            form = CardForm(request.POST)
            if form.is_valid():
                PaymentService.process_payment(order, PaymentMethod.CARD, form.cleaned_data)
                messages.success(request, 'Payment submitted successfully! Awaiting approval.')
                return redirect('payments:success', order_id=order.id)
            card_form = form
            mobile_form = MobileMoneyForm(initial={'amount': order.total_amount})
        else:
            messages.error(request, 'Please select a payment method.')
            return redirect('payments:checkout', order_id=order.id)

        return render(request, self.template_name, {
            'order': order,
            'mobile_form': mobile_form,
            'card_form': card_form,
            'page_title': 'Payment',
        })


class PaymentSuccessView(CustomerRequiredMixin, View):
    template_name = 'public/payment_success.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user.profile)
        return render(request, self.template_name, {
            'order': order,
            'page_title': 'Payment Success',
        })
