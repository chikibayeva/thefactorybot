from django.db import models
from django.contrib.auth.models import User

from tg_bot import managers as bot_managers

class UserChat(models.Model):
    id: int

    chat_id: int = models.IntegerField("chat id", unique=True, null=True)
    token: str = models.CharField("user token", max_length=50)

    user_id: int
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="chat")

    objects = bot_managers.UserChatManager()

    def __str__(self):
        return f"{self.user.username} chat"
