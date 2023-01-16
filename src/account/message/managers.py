import textwrap

from django.contrib.auth.models import User
from django.db import models
from django.db.models import manager

from account import models as account_models


class MessageQuerySet(models.QuerySet):
    def sent(self) -> "MessageQuerySet":
        return self.filter(is_sent=True)

class MessageManager(manager.BaseManager.from_queryset(MessageQuerySet)):
    def create_telegram_messages(self, message: str, user: User) -> list['account_models.Message']:
        username = user.username
        message_chunks = textwrap.wrap(message, 3890)
        message_instances = list()
        for chunk in message_chunks:
            instance = self.create(
                text=chunk,
                user_id=user.pk,
                user_reference=username
            )
            message_instances.append(instance)
        return message_instances