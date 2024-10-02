from django.urls import path

from main.apps import MainConfig
from main.views import index, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView, Mailing_listCreateView, \
    Mailing_listListView, Mailing_listDetailView, Mailing_listUpdateView, Mailing_listDeleteView, \
    Attempt_to_sendCreateView, Attempt_to_sendListView, Attempt_to_sendDetailView, Attempt_to_sendUpdateView, \
    Attempt_to_sendDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/list/', ClientListView.as_view(), name='list_client'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('main/client/<int:pk>/edit/', ClientUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/list/', MessageListView.as_view(), name='list_message'),
    path('message/view/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('main/message/<int:pk>/edit/', MessageUpdateView.as_view(), name='edit_message'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('mailing_list/create/', Mailing_listCreateView.as_view(), name='create_mailing_list'),
    path('mailing_list/list/', Mailing_listListView.as_view(), name='list_mailing_list'),
    path('mailing_list/view/<int:pk>/', Mailing_listDetailView.as_view(), name='view_mailing_list'),
    path('main/mailing_list/<int:pk>/edit/', Mailing_listUpdateView.as_view(), name='edit_mailing_list'),
    path('mailing_list/delete/<int:pk>/', Mailing_listDeleteView.as_view(), name='delete_mailing_list'),
    path('attempt_to_send/create/', Attempt_to_sendCreateView.as_view(), name='create_attempt_to_send'),
    path('attempt_to_send/list/', Attempt_to_sendListView.as_view(), name='list_attempt_to_send'),
    path('attempt_to_send/view/<int:pk>/', Attempt_to_sendDetailView.as_view(), name='view_attempt_to_send'),
    path('main/attempt_to_send/<int:pk>/edit/', Attempt_to_sendUpdateView.as_view(), name='edit_attempt_to_send'),
    path('attempt_to_send/delete/<int:pk>/', Attempt_to_sendDeleteView.as_view(), name='delete_attempt_to_send'),
]

