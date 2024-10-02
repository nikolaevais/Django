from django.contrib import admin
from main.models import Client_servis, Message, Mailing_list, Attempt_to_send
@admin.register(Client_servis)
class Client_servis(admin.ModelAdmin):
    list_display = ("email", "last_name", "first_name")


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Mailing_list)
class Mailing_list(admin.ModelAdmin):
    list_display = ("date_and_time_of_first_attempt", "periodicity", "message")


@admin.register(Attempt_to_send)
class Attempt_to_send(admin.ModelAdmin):
    list_display = ("date_and_time_of_last_attempt", "status_attempt", "mail_server_response")

