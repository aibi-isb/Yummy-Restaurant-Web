from django import forms
from django.contrib.auth.models import User
from apps.core.models import SiteConfiguration


class SiteSettingsForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. admin_hasan'}),
        help_text='This will be your public display name and login username.'
    )
    first_name = forms.CharField(max_length=150, required=False, label='First Name',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, label='Last Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(
        max_length=128, required=False, label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    confirm_password = forms.CharField(
        max_length=128, required=False, label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    class Meta:
        model = SiteConfiguration
        fields = ['restaurant_name', 'logo', 'admin_avatar']
        widgets = {
            'restaurant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. YUMMY Restaurant'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'admin_avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.user.pk).filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        new_pw = cleaned.get('new_password')
        confirm = cleaned.get('confirm_password')
        if new_pw or confirm:
            if new_pw != confirm:
                raise forms.ValidationError('Passwords do not match.')
            if len(new_pw) < 8:
                raise forms.ValidationError('Password must be at least 8 characters.')
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit)
        if self.user:
            self.user.username = self.cleaned_data.get('username', self.user.username)
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            new_pw = self.cleaned_data.get('new_password')
            if new_pw:
                self.user.set_password(new_pw)
            if commit:
                self.user.save()
        return instance
