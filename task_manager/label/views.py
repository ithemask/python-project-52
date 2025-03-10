from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.core.mixins import AuthRequiredMixin
from task_manager.label.forms import LabelForm
from task_manager.label.models import Label


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
    SuccessMessageMixin,
    DeleteView,
):
    model = Label
    template_name = 'label_delete.html'

    success_url = reverse_lazy('label-list')
    success_message = _('Label has been successfully deleted')
    error_message = _('Label cannot be deleted because it is being used')

    def post(self, request, *args, **kwargs):
        if not self.get_object().tasks.exists():
            return super().post(request, *args, **kwargs)
        messages.error(request, self.error_message)
        return redirect('label-list')
