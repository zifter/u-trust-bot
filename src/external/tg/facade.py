import logging
from typing import List

from telegram import Update
from telegram.ext import ContextTypes, Application, MessageHandler, filters

from external.tg.message import Message

logger = logging.getLogger('telegram')


class TelegramFacade:
    def __init__(self, token):
        self.application: Application = Application.builder().token(token).build()

        self.application.add_handler(MessageHandler(filters.VOICE | filters.TEXT, self.receive))
        self._message_processor: List = []

    def add_message_processor(self, processor):
        self._message_processor.append(processor)

    async def reply_on_message(self, msg: Message, text: str):
        logger.info(f'Send message "{text}"')

        await msg.update.message.reply_text(text, parse_mode='HTML')

    async def set_my_commands(self, commands):
        await self.application.bot.set_my_commands(commands)

    def run_polling(self):
        self.application.run_polling()

    def run_webhook(self, port, secret_token, url):
        self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token=secret_token,
            webhook_url=url
        )

    async def receive(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.debug(f'Text {update.message}')

        for processor in self._message_processor:
            await processor(Message(update, context))
