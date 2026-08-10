from django.urls import path
from .views import HomeView, AboutView, MenuListView, FoodDetailView

app_name = 'menu'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('menu/', MenuListView.as_view(), name='list'),
    path('menu/<int:pk>/', FoodDetailView.as_view(), name='detail'),
    # Legacy alias used by older templates (e.g. customer_sidebar)
    path('browse/', MenuListView.as_view(), name='browse'),
]
