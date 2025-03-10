from django.contrib.auth.forms import UserCreationForm, UsernameField
from task_manager.user.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        return self.cleaned_data.get('username')
