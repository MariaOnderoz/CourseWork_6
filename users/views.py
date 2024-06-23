import random
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserModeratorForm
from users.models import User
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect, render
import secrets


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message= f'Для подтверждения почты перейдите по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("users.can_view_user") and user.has_perm("users.can_block_user"):
            return UserModeratorForm
        raise UserProfileForm


def generate_new_password(request):
    CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-'
    new_password = ''
    if request.method == 'POST':
        email = request.POST['email']
        user = get_object_or_404(User, email=email)
        for i in range(10):
            new_password += random.choice(CHARS)
        send_mail(
            subject='Смена пароля',
            message=f'Ваш новый пароль {new_password}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse('users:login'))
    return render(request, 'users/password_reset.html')

