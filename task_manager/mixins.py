from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
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
    edit_error_message = _('You have no permission to edit another user.')
    delete_error_message = _('User cannot be deleted because it is being used')

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request, self.edit_error_message)
            return redirect('user-list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if request.user != self.get_object():
                messages.error(request, self.edit_error_message)
                return redirect('user-list')
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.delete_error_message)
            return redirect('user-list')


class StatusDeleteMixin:
    error_message = _('Status cannot be deleted because it is being used')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect('status-list')


class TaskDeleteMixin:
    error_message = _('Task can be deleted only by the author')

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            messages.error(request, self.error_message)
            return redirect('task-list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            messages.error(request, self.error_message)
            return redirect('task-list')
        return super().post(request, *args, **kwargs)
