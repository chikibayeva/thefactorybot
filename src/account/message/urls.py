from django.urls import path

from . import views

urlpatterns = [
    path("send/", views.SendMessageView.as_view()),
    path("list/", views.MessageListView.as_view()),
]