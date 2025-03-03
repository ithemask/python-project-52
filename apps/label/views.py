from apps.core.mixins import AuthRequiredMixin
from apps.label.forms import LabelForm
from apps.label.mixins import LabelDeleteMixin
from apps.label.models import Label
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    ordering = 'id'
    template_name = 'label_list.html'


class LabelCreateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = LabelForm
    template_name = 'label_create.html'

    success_url = reverse_lazy('label-list')
    success_message = _('Label has been successfully created')


class LabelUpdateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Label
    form_class = LabelForm
    template_name = 'label_update.html'

    success_url = reverse_lazy('label-list')
    success_message = _('Label has been successfully updated')


class LabelDeleteView(
    AuthRequiredMixin,
    LabelDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Label
    template_name = 'label_delete.html'

    success_url = reverse_lazy('label-list')
    success_message = _('Label has been successfully deleted')
