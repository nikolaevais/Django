from django.forms import ModelForm, BooleanField

from main.models import Client_servis, Message, Mailing_list, Attempt_to_send


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class Client_servisForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client_servis
        exclude = ("owner",)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class Mailing_listForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing_list
        exclude = ("owner",)


class Mailing_listModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing_list
        fields = ("is_active",)


class Attempt_to_sendForm(ModelForm):
    class Meta:
        model = Attempt_to_send
        fields = "__all__"
