from apps.core.mixins import AuthRequiredMixin
from apps.status.forms import StatusForm
from apps.status.mixins import StatusDeleteMixin
from apps.status.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
    StatusDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Status
    template_name = 'status_delete.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully deleted')
