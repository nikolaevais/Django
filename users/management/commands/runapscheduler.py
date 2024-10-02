import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from config.settings import EMAIL_HOST_USER
from main.models import Mailing_list, Attempt_to_send

from django.utils import timezone


def my_job():
    current_dt = timezone.now()
    # получение всех активных рассылок
    mailings = Mailing_list.objects.filter(is_active=True)

    for mail in mailings:
        if mail.data_next_shipping:
            mail.date_and_time_of_first_attempt = mail.data_next_shipping

        print(mail.date_and_time_of_first_attempt, current_dt)

        # проверка необходимости рассылки
        if mail.date_and_time_of_first_attempt < current_dt:
            # смена статуса
            mail.status = 'STARTED'

            # создание попытки
            attempt = Attempt_to_send.objects.create(mailing_list=mail)
            try:
                send_mail(
                subject=mail.message.title,
                message=mail.message.description,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email for client in mail.client.all()]
                )


                # Ежедневная рассылка
                if mail.periodicity == 'DAILY':
                    mail.data_next_shipping = current_dt + datetime.timedelta(days=1)
                    mail.save()

                # Еженедельная рассылка
                elif mail.periodicity == 'WEEKLY':
                    mail.data_next_shipping = current_dt + datetime.timedelta(days=7)
                    mail.save()

                # Ежемесячная рассылка
                elif mail.periodicity == 'MONTHLY':
                    mail.data_next_shipping = current_dt + datetime.timedelta(days=30)
                    mail.save()

                print(mail.data_next_shipping)
                print(mail.status)
                attempt.status_attempt = 'success'
                attempt.date_and_time_of_last_attempt = current_dt
                attempt.mail_server_response = "Сообщения отправлены"
                attempt.save()

            except Exception as e:
                attempt.status_attempt = 'failed'
                attempt.date_and_time_of_last_attempt = current_dt
                attempt.mail_server_response = e
                attempt.save()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
             my_job,
             trigger=CronTrigger(minute="*/2"),
             id="send_mailing",  # The `id` assigned to each job MUST be unique
             max_instances=3,
             replace_existing=True,
        )

        try:
             scheduler.start()
        except KeyboardInterrupt:
             scheduler.shutdown()