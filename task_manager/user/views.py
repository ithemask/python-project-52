from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.user.forms import UserCreateForm, UserUpdateForm
from task_manager.user.mixins import UserEditMixin
from task_manager.user.models import User


class UserListView(ListView):
    model = User
    ordering = 'id'
    template_name = 'user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'user_create.html'

    success_url = reverse_lazy('login')
    success_message = _('Account has been successfully created')


class UserUpdateView(
    UserEditMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update.html'

    success_url = reverse_lazy('user-list')
    success_message = _('Account has been successfully updated')


class UserDeleteView(
    UserEditMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    template_name = 'user_delete.html'

    success_url = reverse_lazy('user-list')
    success_message = _('Account has been successfully deleted')
