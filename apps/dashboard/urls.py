from django.urls import path
from .views import (
    AdminDashboardView,
    FoodManagementView, FoodCreateView, FoodUpdateView, FoodDeleteView,
    CategoryManagementView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    CustomerManagementView, CustomerEditView, CustomerDeleteView,
    OrderManagementView, OrderStatusUpdateView,
    PaymentVerificationView, PaymentApproveView, PaymentRejectView,
    NotificationManagementView, NotificationCreateView, NotificationDeleteView,
    SettingsView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='home'),

    # Foods
    path('foods/', FoodManagementView.as_view(), name='foods'),
    path('foods/create/', FoodCreateView.as_view(), name='foods_create'),
    path('foods/<int:pk>/edit/', FoodUpdateView.as_view(), name='foods_edit'),
    path('foods/<int:pk>/delete/', FoodDeleteView.as_view(), name='foods_delete'),

    # Categories
    path('categories/', CategoryManagementView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='categories_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='categories_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='categories_delete'),

    # Customers
    path('customers/', CustomerManagementView.as_view(), name='customers'),
    path('customers/<int:pk>/edit/', CustomerEditView.as_view(), name='customers_edit'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customers_delete'),

    # Orders
    path('orders/', OrderManagementView.as_view(), name='orders'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='orders_status'),

    # Payments
    path('payments/', PaymentVerificationView.as_view(), name='payments'),
    path('payments/<int:pk>/approve/', PaymentApproveView.as_view(), name='payments_approve'),
    path('payments/<int:pk>/reject/', PaymentRejectView.as_view(), name='payments_reject'),

    # Notifications
    path('notifications/', NotificationManagementView.as_view(), name='notifications'),
    path('notifications/create/', NotificationCreateView.as_view(), name='notifications_create'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notifications_delete'),

    # Settings
    path('settings/', SettingsView.as_view(), name='settings'),
]
