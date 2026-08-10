from django.views.generic import ListView, DetailView, TemplateView
from .models import Food, FoodCategory
from .services import SearchService
from apps.core.constants import DEFAULT_PAGE_SIZE


class HomeView(TemplateView):
    template_name = 'public/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_foods'] = Food.objects.filter(featured=True, is_available=True)[:6]
        context['categories'] = FoodCategory.objects.all()
        context['page_title'] = 'YUMMI Restaurant'
        return context


class AboutView(TemplateView):
    template_name = 'public/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'
        return context


class MenuListView(ListView):
    model = Food
    template_name = 'public/menu_browse.html'
    context_object_name = 'foods'
    paginate_by = DEFAULT_PAGE_SIZE

    _SORT_MAP = {
        'price-asc': 'price',
        'price-desc': '-price',
        'name': 'name',
    }

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        category_id = self.request.GET.get('category', '')
        category = FoodCategory.objects.filter(id=category_id).first() if category_id else None
        qs = SearchService.search(query=query, category=category)

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if self.request.GET.get('available_only', '1') != '0':
            qs = qs.filter(is_available=True)

        sort = self.request.GET.get('sort', '')
        ordering = self._SORT_MAP.get(sort, 'name')
        return qs.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoodCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('query', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        context['price_min'] = self.request.GET.get('price_min', '')
        context['price_max'] = self.request.GET.get('price_max', '')
        context['available_only'] = self.request.GET.get('available_only', '1') != '0'
        if context['selected_category']:
            cat = FoodCategory.objects.filter(id=context['selected_category']).first()
            context['selected_category_name'] = cat.name if cat else ''
        else:
            context['selected_category_name'] = ''
        context['has_active_filters'] = bool(
            context['search_query']
            or context['selected_category']
            or context['price_min']
            or context['price_max']
            or not context['available_only']
            or context['selected_sort']
        )
        context['page_title'] = 'Menu'
        return context


class FoodDetailView(DetailView):
    model = Food
    template_name = 'public/menu_item.html'
    context_object_name = 'food'

    def get_queryset(self):
        return Food.objects.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_foods'] = Food.objects.filter(
            category=self.object.category, is_available=True
        ).exclude(id=self.object.id)[:8]
        context['page_title'] = self.object.name
        return context
