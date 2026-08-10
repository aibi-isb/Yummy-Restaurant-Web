from django.contrib import admin
from .models import FoodCategory, Food


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    list_display = ['name', 'created_at']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'featured']
    list_filter = ['category', 'is_available', 'featured']
    search_fields = ['name', 'description']
