from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.core.mixins import AuthRequiredMixin
from task_manager.task.forms import TaskForm, TaskFilterForm
from task_manager.task.models import Task


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    ordering = 'id'
    template_name = 'task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        executor = self.request.GET.get('executor')
        label = self.request.GET.get('label')
        self_tasks = self.request.GET.get('self_tasks')
        if self_tasks:
            queryset = queryset.filter(author=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        if executor:
            queryset = queryset.filter(executor=executor)
        if label:
            queryset = queryset.filter(labels=label)
        return queryset


class TaskCreateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    form_class = TaskForm
    template_name = 'task_create.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully created')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'


class TaskUpdateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully updated')


class TaskDeleteView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    template_name = 'task_delete.html'

    success_url = reverse_lazy('task-list')
    success_message = _('Task has been successfully deleted')
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
