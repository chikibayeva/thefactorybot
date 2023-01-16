from django.urls import path, include

urlpatterns = [
    path("token/", include("account.token.urls")),
    path("message/", include("account.message.urls")),
]