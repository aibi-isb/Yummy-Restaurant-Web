from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import RegisterForm


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('menu:home')

    def post(self, request):
        auth_logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('menu:home')


class RegisterView(View):
    template_name = 'public/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('dashboard:home')
            return redirect('menu:home')
        form = RegisterForm()
        return render(request, self.template_name, self._get_context(form))

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. Please sign in.')
            return redirect('auth:login')
        return render(request, self.template_name, self._get_context(form))

    def _get_context(self, form):
        demo = User.objects.filter(is_staff=False).order_by('?').first()
        return {'form': form, 'page_title': 'Register', 'demo_username': demo.username if demo else ''}


class CustomLoginView(LoginView):
    template_name = 'public/login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('dashboard:home')
        return reverse('menu:home')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        demo = User.objects.filter(is_staff=False).order_by('?').first()
        context['demo_username'] = demo.username if demo else ''
        return context


class ForgotPasswordView(View):
    template_name = 'public/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': PasswordResetForm(), 'page_title': 'Forgot Password'})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            messages.success(request, 'If an account exists for that email, a reset link has been sent.')
            return redirect('auth:login')
        return render(request, self.template_name, {'form': form, 'page_title': 'Forgot Password'})


class ResetPasswordView(View):
    template_name = 'public/reset_password.html'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, 'Please sign in to reset your password, or use the link from your email.')
            return redirect('auth:login')
        return render(request, self.template_name, {'form': SetPasswordForm(request.user), 'page_title': 'Reset Password'})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('menu:home')
        return render(request, self.template_name, {'form': form, 'page_title': 'Reset Password'})
