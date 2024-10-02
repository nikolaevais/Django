import random

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from main.forms import Client_servisForm, MessageForm, Mailing_listForm, Attempt_to_sendForm, Mailing_listModeratorForm
from main.models import Client_servis, Message, Mailing_list, Attempt_to_send


#@permission_required('main.view_mailing_list')
def index(request):
    mailings_count = cache.get('mailings_count')
    if mailings_count is None:
        mailings_count = Mailing_list.objects.count()
        cache.set('mailings_count', mailings_count, 60)

    mailings_is_active_count = cache.get('mailings_is_active_count')
    if mailings_is_active_count is None:
        mailings_is_active_count = Mailing_list.objects.filter(is_active=True).count()
        cache.set('mailings_is_active_count', mailings_is_active_count, 60)

    unique_clients_count = cache.get('unique_clients_count')
    if unique_clients_count is None:
        unique_clients_count = Client_servis.objects.values('email').distinct().count()
        cache.set('unique_clients_count', unique_clients_count, 60)

    blogs = Blog.objects.all()
    if len(blogs) >= 3:
        random_blogs = random.sample(list(blogs), 3)
    else:
        random_blogs = blogs

    context = {
        'mailings_count': mailings_count,
        'mailings_is_active_count': mailings_is_active_count,
        'unique_clients_count': unique_clients_count,
        'random_blogs': random_blogs
    }
    return render(request, 'main/index.html', context)


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client_servis
    form_class = Client_servisForm
    success_url = reverse_lazy('main:list_client')

    def form_valid(self, form):
        client_servis = form.save()
        user = self.request.user
        client_servis.owner = user
        client_servis.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client_servis


class ClientDetailView(DetailView):
    model = Client_servis


class ClientUpdateView(UpdateView):
    model = Client_servis
    form_class = Client_servisForm
    success_url = reverse_lazy('main:list_client')


class ClientDeleteView(DeleteView):
    model = Client_servis
    success_url = reverse_lazy('main:list_client')


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:list_message')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:list_message')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:list_message')


class Mailing_listCreateView(CreateView, LoginRequiredMixin):
    model = Mailing_list
    form_class = Mailing_listForm
    success_url = reverse_lazy('main:list_mailing_list')

    def form_valid(self, form):
        mailing_list = form.save()
        user = self.request.user
        mailing_list.owner = user
        mailing_list.save()
        return super().form_valid(form)


class Mailing_listListView(ListView):
    model = Mailing_list


class Mailing_listDetailView(DetailView):
    model = Mailing_list


class Mailing_listUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing_list
    form_class = Mailing_listForm
    success_url = reverse_lazy('main:list_mailing_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return Mailing_listForm
        if user.has_perm('set_active'):
            return Mailing_listModeratorForm
        raise PermissionDenied


class Mailing_listDeleteView(DeleteView):
    model = Mailing_list
    success_url = reverse_lazy('main:list_mailing_list')


class Attempt_to_sendCreateView(CreateView):
    model = Attempt_to_send
    form_class = Attempt_to_sendForm
    success_url = reverse_lazy('main:list_attempt_to_send')


class Attempt_to_sendListView(ListView):
    model = Attempt_to_send


class Attempt_to_sendDetailView(DetailView):
    model = Attempt_to_send


class Attempt_to_sendUpdateView(UpdateView):
    model = Attempt_to_send
    form_class = Attempt_to_sendForm
    success_url = reverse_lazy('main:list_attempt_to_send')


class Attempt_to_sendDeleteView(DeleteView):
    model = Attempt_to_send
    success_url = reverse_lazy('main:list_attempt_to_send')
