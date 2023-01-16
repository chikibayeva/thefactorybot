from django.db import models
from django.db.models import manager


class UserChatQuerySet(models.QuerySet):
    ...

class UserChatManager(manager.BaseManager.from_queryset(UserChatQuerySet)):
    ...