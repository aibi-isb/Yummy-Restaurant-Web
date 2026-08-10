from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'address', 'phone_number', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'e.g. John Doe',
                'class': 'profile-input',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g. +232 76 123 456',
                'class': 'profile-input',
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '123 Main Street, Freetown',
                'class': 'profile-input profile-textarea',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        help_texts = {
            'full_name': 'Your full name as it appears on orders.',
            'phone_number': 'Used for delivery contact.',
            'address': 'Your default delivery address.',
        }
