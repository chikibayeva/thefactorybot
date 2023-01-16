import asyncio

from celery import Task
from django.conf import settings
from django.contrib.auth.models import User

from account import models as account_models
from app.celery import app
from tg_bot.bot.bot import Bot


class SendMessages(Task):
    queue = 'thefactorybot-celery'

    def run(self, user_id: int, messages_id: list[int]) -> None:
        bot = Bot(settings.BOT_TOKEN)
        user = User.objects.select_related('chat').get(id=user_id)

        for message_id in messages_id:
            message = account_models.Message.objects.get(id=message_id)
            asyncio.run(bot.send_msg(user.chat.chat_id, message.text, user.username))
            message.mark_sent()


send_messages = app.register_task(SendMessages())
