from asgiref.sync import sync_to_async
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters, ConversationHandler,
)

from tg_bot import models as bot_models


AUTH_STATE = 0

class Bot:
    application: Application | None
    AUTH_STATE = 0

    def __init__(self, token, *args, **kwargs):
        if not token:
            return

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('token', self.get_token)],
            states={
                self.AUTH_STATE:[MessageHandler(filters.TEXT, self.token_handler),]
            },
            fallbacks=[
                CommandHandler('start', self.start)],
            name='auth_conv'
        )

        self.application = Application.builder().token(token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(conv_handler)
        # self.application.add_handler(
        #     MessageHandler(filters.TEXT & ~filters.COMMAND, self.send_msg)
        # )


    async def start(self, update: Update) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(
        self, update: Update) -> None:
        await update.message.reply_text("Help!")

    async def get_token(self, update: Update, context: ContextTypes) -> None:
        await update.message.reply_text("Please enter your token")
        return self.AUTH_STATE

    async def token_handler(self, update: Update, context: ContextTypes) -> int:
        input_token = update.message.text
        user_chat = await bot_models.UserChat.objects.filter(token=input_token).afirst()

        if not user_chat:
            await update.message.reply_text("Token was not found")
            return self.AUTH_STATE

        chat_id =  update.message.chat_id
        user_chat.chat_id = chat_id
        await sync_to_async(user_chat.save)()


        await update.message.reply_text("Token was found successfully. Messages will now be sent to this chat.")
        return self.AUTH_STATE

    async def send_msg(self, chat_id: int, message: str, username: str) -> None:
        telegram_message = f"{username}, я получил от тебя сообщение:\n{message}"
        print(message)
        await self.application.bot.send_message(chat_id, telegram_message)
