from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager import models


class UserCreateForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username']
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        return self.cleaned_data.get('username')


class StatusForm(ModelForm):
    class Meta:
        model = models.Status
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
        error_messages = {
            'name': {
                'unique': _('Status with such name already exists.'),
                'max_length': _('Name is too long. '
                                'Maximum length is 50 characters.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True


class TaskForm(ModelForm):
    class Meta:
        model = models.Task
        exclude = ['author']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
        }
        error_messages = {
            'name': {
                'unique': _('Task with such name already exists.'),
                'max_length': _('Name is too long. '
                                'Maximum length is 100 characters.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        models.Status.objects.all(),
        label=_('Status'),
        required=False,
    )
    executor = forms.ModelChoiceField(
        models.User.objects.all(),
        label=_('Executor'),
        required=False,
    )
    self_tasks = forms.BooleanField(
        label=_('Only my tasks'),
        required=False,
    )
