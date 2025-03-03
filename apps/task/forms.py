from apps.label.models import Label
from apps.status.models import Status
from apps.task.models import Task
from apps.user.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['author']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels'),
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
        Status.objects.all(),
        label=_('Status'),
        required=False,
    )
    executor = forms.ModelChoiceField(
        User.objects.all(),
        label=_('Executor'),
        required=False,
    )
    label = forms.ModelChoiceField(
        Label.objects.all(),
        label=_('Label'),
        required=False,
    )
    self_tasks = forms.BooleanField(
        label=_('Only my tasks'),
        required=False,
    )
