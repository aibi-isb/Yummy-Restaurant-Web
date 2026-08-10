from django.urls import path
from .views import CustomerDashboardView, CustomerProfileView, CustomerProfileEditView

app_name = 'customers'

urlpatterns = [
    path('', CustomerDashboardView.as_view(), name='dashboard'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('profile/edit/', CustomerProfileEditView.as_view(), name='profile_edit'),
]
