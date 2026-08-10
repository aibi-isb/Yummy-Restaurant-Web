from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class PreventStaffMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return False
        return True

    def handle_no_permission(self):
        return redirect('dashboard:home')


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('auth:login')
        return redirect('menu:home')


class CustomerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_staff:
            return False
        return hasattr(self.request.user, 'profile')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('auth:login')
        if self.request.user.is_staff:
            return redirect('dashboard:home')
        return redirect('auth:login')
