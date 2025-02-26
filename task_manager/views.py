from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager import forms, mixins, models


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
    model = models.User
    ordering = 'id'
    template_name = 'user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreateForm
    template_name = 'user_create.html'

    success_url = reverse_lazy('login')
    success_message = _('Account has been successfully created')


class UserUpdateView(
    mixins.AuthRequiredMixin,
    mixins.UserEditMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = models.User
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
    model = models.User
    template_name = 'user_delete.html'

    success_url = reverse_lazy('user-list')
    success_message = _('Account has been successfully deleted')


class StatusListView(mixins.AuthRequiredMixin, ListView):
    model = models.Status
    ordering = 'id'
    template_name = 'status_list.html'


class StatusCreateView(
    mixins.AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = forms.StatusForm
    template_name = 'status_create.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully created')


class StatusUpdateView(
    mixins.AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = models.Status
    form_class = forms.StatusForm
    template_name = 'status_update.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully updated')


class StatusDeleteView(
    mixins.AuthRequiredMixin,
    mixins.StatusDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = models.Status
    template_name = 'status_delete.html'

    success_url = reverse_lazy('status-list')
    success_message = _('Status has been successfully deleted')


class TaskListView(mixins.AuthRequiredMixin, ListView):
    model = models.Task
    ordering = 'id'
    template_name = 'task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.TaskFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        executor = self.request.GET.get('executor')
        self_tasks = self.request.GET.get('self_tasks')
        if self_tasks:
            queryset = queryset.filter(author=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        if executor:
            queryset = queryset.filter(executor=executor)
        return queryset


class TaskCreateView(
    mixins.AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = forms.TaskForm
    template_name = 'task_create.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully created')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(mixins.AuthRequiredMixin, DetailView):
    model = models.Task
    template_name = 'task_detail.html'


class TaskUpdateView(
    mixins.AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'task_update.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully updated')


class TaskDeleteView(
    mixins.AuthRequiredMixin,
    mixins.TaskDeleteMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = models.Task
    template_name = 'task_delete.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully deleted')
