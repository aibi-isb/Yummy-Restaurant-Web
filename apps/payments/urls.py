from django.urls import path
from .views import PaymentView, PaymentSuccessView

app_name = 'payments'

urlpatterns = [
    path('<int:order_id>/', PaymentView.as_view(), name='checkout'),
    path('success/<int:order_id>/', PaymentSuccessView.as_view(), name='success'),
]
