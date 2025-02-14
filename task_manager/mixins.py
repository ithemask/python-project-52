from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not authorized! Please log in to your account.'),
        )
        return super().handle_no_permission()


class UserEditMixin:
    error_message = _('You have no permission to edit another user.')

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request, self.error_message)
            return redirect('user-list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request, self.error_message)
            return redirect('user-list')
        return super().post(request, *args, **kwargs)
