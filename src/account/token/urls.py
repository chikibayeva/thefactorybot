from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.CreateChatTokenView.as_view()),
    path("<int:chat_id>/update/", views.UpdateChatTokenView.as_view()),
    path("get/", views.GetChatTokenView.as_view()),
]