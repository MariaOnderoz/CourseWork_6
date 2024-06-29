from apscheduler.schedulers.background import BlockingScheduler
import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from mailing.models import MailSettings, MailingAttempt

period_mailing = ["Раз в день", "Раз в неделю", "Раз в месяц"]


def send_mailing():
    """Функция отправки рассылки"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = MailSettings.objects.filter(status="Запущена")

    for mailing in mailings:

        if mailing.send_time <= current_datetime:
            status = False
            server_responce = "Нет ответа"

            try:
                recipient_emails = [client.email for client in mailing.client.all()]
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=recipient_emails,
                    fail_silently=False
                )

                if mailing.frequency == period_mailing[0]:
                    mailing.send_time += timedelta(days=1)
                elif mailing.frequency == period_mailing[1]:
                    mailing.send_time += timedelta(weeks=1)
                elif mailing.frequency == period_mailing[2]:
                    mailing.send_time += timedelta(days=30)

                mailing.save()

                status = True
                server_responce = "Успешно"

            except smtplib.SMTPResponseException as response:
                status = False
                server_responce = str(response)

            finally:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=status,
                    server_response=server_responce,
                )


def start():
    """Функция запуска алгоритма отправки рассылки"""
    scheduler = BlockingScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()

