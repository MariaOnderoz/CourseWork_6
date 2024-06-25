import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from random import sample
from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailSettingsForm, MailSettingsModeratorForm
from mailing.models import Client, Message, MailSettings, MailingAttempt


class HomePage(TemplateView):
    """Контроллер главной страницы"""

    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["mailing_count"] = MailSettings.objects.all().count()
        context_data["active_mailing_count"] = MailSettings.objects.filter(status__in=['created', 'started']).count()
        context_data["unique_clients_count"] = Client.objects.all().distinct('email').count()
        all_posts = list(Blog.objects.all())
        context_data['random_posts'] = sample(all_posts, min(len(all_posts), 3))
        return context_data


# Классы для клиентов

class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер списка клиентов"""

    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детального просмотра клиента"""

    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования клиента"""

    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления клиента"""

    model = Client
    success_url = reverse_lazy('mailing:client_list')


# Классы для сообщений

class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер списка сообщений"""

    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детального просмотра сообщения"""

    model = Message

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования сообщения"""

    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления сообщения"""

    model = Message
    success_url = reverse_lazy('mailing:message_list')


# Классы для настройки рассылки

class MailSettingsCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания настройки рассылки"""

    model = MailSettings
    form_class = MailSettingsForm
    success_url = reverse_lazy('mailing:mail_settings_list')

    def form_valid(self, form):
        mail_settings = form.save()
        user = self.request.user
        mail_settings.owner = user
        mail_settings.save()
        return super().form_valid(form)


class MailSettingsListView(LoginRequiredMixin, ListView):
    """Контроллер списка настроек рассылки"""

    model = MailSettings


class MailSettingsDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детального просмотра настройки рассылки"""

    model = MailSettings

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class MailSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования настройки рассылки"""

    model = MailSettings
    form_class = MailSettingsForm

    def get_success_url(self):
        return reverse_lazy('mailing:mail_settings_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailSettingsForm
        if user.has_perm("maılıng.can_view_mail_settings") and user.has_perm("maılıng.can_disable_mail_settings"):
            return MailSettingsModeratorForm
        raise PermissionDenied


class MailSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления настройки рассылки"""

    model = MailSettings
    success_url = reverse_lazy('mailing:mail_settings_list')


# Классы для попыток рассылки


class MailingAttemptListView(LoginRequiredMixin, ListView):
    """Контроллер списка попыток рассылки"""

    model = MailingAttempt
    template_name ='mailing/mailing_attempt_list.html'

    

