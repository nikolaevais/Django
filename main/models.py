from django.db import models

from config import settings
from users.models import NULLABLE


class Client_servis(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Отчество", **NULLABLE)
    comments = models.TextField(verbose_name="Комментарии", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name="Тема письма")
    description = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title


class Mailing_list(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    )

    FREQUENCY_CHOICES = (
        ('DAILY', 'раз в день'),
        ('WEEKLY', 'раз в неделю'),
        ('MONTHLY', 'раз в месяц'),
    )

    name = models.CharField(max_length=50, verbose_name="Название рассылки", **NULLABLE)
    date_and_time_of_first_attempt = models.DateTimeField(auto_now_add=True,
                                                          verbose_name="Дата первой отправки рассылки")
    periodicity = models.CharField(max_length=25, verbose_name="Периодичность", choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=25, verbose_name="Статус", choices=STATUS_CHOICES, default='Создана')
    data_next_shipping = models.DateTimeField(verbose_name="Дата следующей отправки", **NULLABLE)

    message = models.OneToOneField(Message, on_delete=models.CASCADE, primary_key=True, verbose_name="Сообщение",
                                   related_name="messages")
    client = models.ManyToManyField(Client_servis, verbose_name="Клиенты", related_name="client")
    is_active = models.BooleanField(default=True, verbose_name='активная')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)


    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('set_active', 'Can active mailing_list')
        ]

    def __str__(self):
        return self.name


class Attempt_to_send(models.Model):
    date_and_time_of_last_attempt = models.DateTimeField(verbose_name="Дата и время последней отправки", **NULLABLE)
    status_attempt = models.CharField(max_length=20, verbose_name="Статус попытки", **NULLABLE)
    mail_server_response = models.CharField(max_length=50, verbose_name="Ответ почтового сервера", **NULLABLE)
    mailing_list = models.ForeignKey(Mailing_list, on_delete=models.SET_NULL, verbose_name="Рассылка", **NULLABLE,
                                     related_name="mailing_list")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"

    def __str__(self):
        return self.mailing_list
