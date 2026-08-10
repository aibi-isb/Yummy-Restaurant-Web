from django.urls import path
from .views import CartView, CheckoutView, OrderTrackingView, OrderDetailView, clear_order_history

app_name = 'orders'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderTrackingView.as_view(), name='list'),
    path('orders/<int:pk>/track/', OrderDetailView.as_view(), name='track'),
    path('orders/clear-history/', clear_order_history, name='clear_history'),
]
