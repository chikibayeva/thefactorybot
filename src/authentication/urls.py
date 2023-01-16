from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginApiView.as_view()),
    path("registration/", views.UserRegistrationView.as_view()),
    path("logout/", views.LogOutView.as_view()),
]
