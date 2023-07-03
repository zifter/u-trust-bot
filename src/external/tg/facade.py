import logging
import pickle
from dataclasses import dataclass
from typing import List

from telegram import Update
from telegram._utils.types import ReplyMarkup
from telegram.ext import ContextTypes, Application, MessageHandler, filters, CallbackQueryHandler

from external.tg.message import Message, CallbackQuery

logger = logging.getLogger('telegram')



class TelegramFacade:
    def __init__(self, token):
        self.application: Application = Application.builder().token(token).build()
        self._message_processors: List = []
        self._callback_processors: List = []

        self.application.add_handler(MessageHandler(filters.VOICE | filters.TEXT, self.receive_message))
        self.application.add_handler(CallbackQueryHandler(self.receive_callback))

    def add_message_processor(self, message_processor):
        self._message_processors.append(message_processor)

    def add_callback_processor(self, process_callback):
        self._callback_processors.append(process_callback)

    async def receive_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.debug(f'Message {update.message}')

        for processor in self._message_processors:
            await processor(Message(update, context))

    async def receive_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.debug(f'Callback {update.message}')

        for callback in self._callback_processors:
            await callback(CallbackQuery(update, context))

    async def reply_on_message(self, msg: Message, text: str, reply_markup: ReplyMarkup):
        logger.info(f'Send message "{text}"')

        await msg.update.message.reply_text(text, parse_mode='HTML', reply_markup=reply_markup)

    async def set_my_commands(self, commands):
        await self.application.bot.set_my_commands(commands)

    async def delete_message(self, chat_id: int, message_id: int):
        await self.application.bot.delete_message(chat_id=chat_id, message_id=message_id)

    def run_polling(self):
        self.application.run_polling()

    def run_webhook(self, port, secret_token, url):
        self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            secret_token=secret_token,
            webhook_url=url
        )
