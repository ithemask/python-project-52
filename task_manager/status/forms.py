from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager.status.models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
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
