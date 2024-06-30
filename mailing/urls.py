from django.urls import path
from mailing.apps import MailingConfig
from django.views.decorators.cache import cache_page
from mailing.views import HomePage, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailSettingsListView, MailSettingsDetailView, MailSettingsCreateView, MailSettingsUpdateView, \
    MailSettingsDeleteView, MailingAttemptListView

app_name = MailingConfig.name


urlpatterns = [
    path('', HomePage.as_view(), name='home'),

    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mail_settings/', MailSettingsListView.as_view(), name='mail_settings_list'),
    path('mail_settings/<int:pk>/', MailSettingsDetailView.as_view(), name='mail_settings_detail'),
    path('mail_settings/create/', MailSettingsCreateView.as_view(), name='mail_settings_create'),
    path('mail_settings/<int:pk>/update/', MailSettingsUpdateView.as_view(), name='mail_settings_update'),
    path('mail_settings/<int:pk>/delete/', MailSettingsDeleteView.as_view(), name='mail_settings_delete'),

    path('mailing_attempt/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
]
