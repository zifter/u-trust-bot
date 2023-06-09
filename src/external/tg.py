import logging
from typing import List

from telegram import Update
from telegram.ext import ContextTypes, Application, MessageHandler, filters

from utils.fs import TEST_DATA_DIR

logger = logging.getLogger('telegram')


class Message:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context

    async def save_voice_file(self, destination):
        new_file = await self.context.bot.get_file(self.update.message.voice.file_id)
        await new_file.download_to_drive(destination)
        return destination


class TelegramFacade:
    def __init__(self, token):
        self.application: Application = Application.builder().token(token).build()

        self.application.add_handler(MessageHandler(filters.VOICE, self.receive))
        self._message_processor: List = []

    def add_message_processor(self, processor):
        self._message_processor.append(processor)

    def get_audio_message_file(self):
        logger.info(f'get audio message file')

        result_file = TEST_DATA_DIR / 'audio' / 'audio_call_mama.ogg'
        logger.info(f'save to {result_file}')
        return result_file

    async def send_text_message(self, msg: Message, text: str):
        logger.info(f'Send message "{text}"')

        await msg.update.message.reply_text(text)

    def run_polling(self):
        self.application.run_polling()

    async def receive(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info(f'Text {update.message}')

        for processor in self._message_processor:
            await processor(Message(update, context))
