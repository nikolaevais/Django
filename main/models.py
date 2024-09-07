from django.db import models

from users.models import NULLABLE

class Client_servis(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Отчество", **NULLABLE)
    comments = models.TextField(verbose_name="Комментарии", **NULLABLE)


    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name="Тема письма")
    description = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title



class Mailing_list(models.Model):
    date_and_time_of_first_attempt = models.DateTimeField(auto_now_add=True, verbose_name="Дата первой отправки рассылки")
    periodicity = models.CharField(max_length=25, verbose_name="Периодичность")
    status = models.CharField(max_length=25, verbose_name="Статус")
    data_next_shipping = models.DateTimeField(verbose_name="Дата следующей отправки")


    message = models.OneToOneField(Message, on_delete=models.CASCADE, primary_key=True, verbose_name="Сообщение", related_name="message")
    client = models.ForeignKey(Client_servis, on_delete=models.SET_NULL, verbose_name="Клиент", **NULLABLE, related_name="client")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


    def __str__(self):
        return self.status



class Attempt_to_send(models.Model):
    date_and_time_of_last_attempt = models.DateTimeField(verbose_name="Дата и время следующей отправки")
    status_attempt = models.CharField(max_length=20, verbose_name="Статус попытки")
    mail_server_response = models.CharField(max_length=50, verbose_name="Ответ почтового сервера")
    mailing_list = models.ForeignKey(Mailing_list, on_delete=models.SET_NULL, verbose_name="Рассылка", **NULLABLE, related_name="mailing_list")


    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"


    def __str__(self):
        return self.status_attempt
