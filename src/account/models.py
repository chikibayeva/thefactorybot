import datetime

from django.contrib.auth.models import User
from django.db import models

from account.message import managers as message_managers


class Message(models.Model):
    id: int

    created_at: datetime.datetime = models.DateTimeField("Creation date", auto_now_add=True, db_index=True)

    text: str = models.TextField("Message text", max_length=4096, null=True, blank=True)
    is_sent: bool = models.BooleanField("Sent to telegram chat", default=False)

    user_id: int
    user: User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='messages')
    user_reference: str = models.CharField("Username", max_length=150, null=True, blank=True)

    objects = message_managers.MessageManager()

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def mark_sent(self):
        self.is_sent = True
        self.save(update_fields=['is_sent'])

    def __str__(self):
        return f"{self.user} message at {self.created_at}"
