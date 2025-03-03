from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


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
