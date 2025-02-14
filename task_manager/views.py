from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager import forms, mixins


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')

    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().post(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    ordering = 'id'
    template_name = 'user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = forms.SignUpForm
    template_name = 'user_create.html'

    success_url = reverse_lazy('login')
    success_message = _('Account has been successfully created')


class UserUpdateView(
    mixins.AuthRequiredMixin,
    mixins.UserEditMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    form_class = forms.UserUpdateForm
    template_name = 'user_update.html'

    success_url = reverse_lazy('user-list')
    success_message = _('Account has been successfully updated')


class UserDeleteView(
    mixins.AuthRequiredMixin,
    mixins.UserEditMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    template_name = 'user_delete.html'

    success_url = reverse_lazy('user-list')
    success_message = _('Account has been successfully deleted')
