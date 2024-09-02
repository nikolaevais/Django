import secrets

from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(19)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтвердите регистрацию на Aririn",
            message=f"Добро пожаловать! "
                    f"Мы рады приветствовать вас и хотим помочь быстрее во всем разобраться. "
                    f"Активируйте аккаунт, чтобы работать с сайтом, для этого перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))






