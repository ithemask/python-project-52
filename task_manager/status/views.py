from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.core.mixins import AuthRequiredMixin
from task_manager.status.forms import StatusForm
from task_manager.status.models import Status


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    ordering = 'id'
    template_name = 'status_list.html'


class StatusCreateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = StatusForm
    template_name = 'status_create.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully created')


class StatusUpdateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    template_name = 'status_update.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully updated')


class StatusDeleteView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Status
    template_name = 'status_delete.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully deleted')
    error_message = _('Status cannot be deleted because it is being used')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect('status-list')
