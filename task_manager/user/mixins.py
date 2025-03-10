from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from task_manager.core.mixins import AuthRequiredMixin


class UserEditMixin(AuthRequiredMixin, UserPassesTestMixin):
    edit_error_message = _('You have no permission to edit another user.')
    delete_error_message = _('User cannot be deleted because it is being used')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, self.edit_error_message)
        return redirect('user-list')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.delete_error_message)
            return redirect('user-list')
