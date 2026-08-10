from django.db.models import Q
from .models import Food


class SearchService:
    @staticmethod
    def search(query=None, category=None):
        foods = Food.objects.filter(is_available=True)
        if query:
            foods = foods.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        if category:
            foods = foods.filter(category=category)
        return foods
