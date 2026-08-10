from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from apps.customers.models import CustomerProfile


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'address', 'phone_number']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        profile = CustomerProfile(
            user=user,
            full_name=self.cleaned_data['full_name'],
            address=self.cleaned_data['address'],
            phone_number=self.cleaned_data['phone_number'],
        )
        if commit:
            profile.save()
        return profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
