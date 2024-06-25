from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from mailing.forms import StyleFormMixin
from users.models import User
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    """Форма редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserModeratorForm(StyleFormMixin, UserChangeForm):
    """Форма модератора для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',]

