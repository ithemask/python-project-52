from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from task_manager import models


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        field_classes = {'username': UsernameField}


class UserUpdateForm(SignUpForm):
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
