import os

from django.core.management.base import BaseCommand

from tg_bot.bot.bot import Bot


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bot = Bot(os.getenv("BOT_TOKEN"))
        bot.application.run_polling()
