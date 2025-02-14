from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User


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
