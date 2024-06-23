from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    """Модель клиента"""
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f' {self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Модель сообщения"""
    subject = models.CharField(max_length=100, verbose_name='Тема письма', **NULLABLE)
    content = models.TextField(verbose_name='Тело письма', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.subject}: {self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailSettings(models.Model):
    """Модель настройки рассылки"""

    periods = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
        ]

    statuses = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
        ]

    send_time = models.DateTimeField(verbose_name='Время отправки рассылки')
    periodicity = models.CharField(max_length=50, choices=periods, verbose_name='Периодичность')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    status = models.CharField(max_length=50, choices=statuses, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.client} {self.send_time}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'

        permissions = [
            ('can_view_mail_settings', 'Может просматривать рассылки'),
            ('can_disable_mail_settings', 'Может отключать рассылки')
        ]


class MailingAttempt(models.Model):
    """Модель с логами рассылки"""

    statuses = [
        ('successful', 'Успешно'),
        ('unsuccessful', 'Не успешно'),
        ]

    last_sending = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=50, choices=statuses, verbose_name='Статус попытки')
    server_responce = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)
    mail_settings = models.ForeignKey(MailSettings, on_delete=models.CASCADE, verbose_name='Настройка рассылки')

    def __str__(self):
        return f'{self.last_sending} {self.status}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'


