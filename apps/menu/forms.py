from django import forms
from .models import Food, FoodCategory


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'category', 'description', 'price', 'image', 'is_available', 'featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Margherita Pizza',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the ingredients, taste, and portion...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',
            }),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search foods...'}))
    category = forms.ModelChoiceField(queryset=FoodCategory.objects.all(), required=False, empty_label='All categories')
