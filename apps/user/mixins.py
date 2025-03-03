from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


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
