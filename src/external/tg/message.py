import logging
from enum import Enum

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger('telegram')


class MessageContentType(Enum):
    NONE = 0
    COMMAND = 1
    TEXT = 2
    VOICE = 3


class Message:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context

    @property
    def content_type(self) -> MessageContentType:
        if self.update.message.text:
            if self.update.message.text.startswith('/'):
                return MessageContentType.COMMAND
            else:
                return MessageContentType.TEXT
        elif self.update.message.voice:
            return MessageContentType.VOICE
        else:
            return MessageContentType.NONE

    @property
    def text(self) -> str:
        return self.update.message.text

    @property
    def telegram_id(self):
        return self.update.message.from_user.id

    async def save_voice_file(self, destination):
        new_file = await self.context.bot.get_file(self.update.message.voice.file_id)
        await new_file.download_to_drive(destination)
        return destination

    def vo_duration(self) -> int:
        return self.update.message.voice.duration
