import abc
from datetime import datetime

from external.db.types import User, Registration
from utils.st import rand_string_id
from utrust.commands.base import MessageCommandBase, UserCommandBase

from utrust.context import UserCommandContext


class ProcessMessageCommand(MessageCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        user: User = self.external.db.get_user(self.message.telegram_id)
        if user is None:
            user = User(
                telegram_id=self.message.telegram_id,
                registration=Registration(
                    created_at=datetime.now()
                )
            )
            self.external.db.create_user(user)

        user_context = UserCommandContext(user, self.message_context)

        if user.registration.confirmed:
            return AuthorizeUserCommand(user_context)

        return SpeechToTextCommand(user_context)


class AuthorizeUserCommand(UserCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        return SendTextMessageToUserCommand('You are not authorized', self.user_context)


class SpeechToTextCommand(UserCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    async def do_exec(self):
        audio_file_path = self.tmp_dir / rand_string_id(prefix='audio-', suffix='.ogg')

        audio_file = await self.message.save_voice_file(audio_file_path)
        audio_url = self.external.gcp.upload_to_bucket(audio_file)
        text = self.external.gcp.speech_to_text(audio_url)

        return SendTextMessageToUserCommand(text, self.user_context)


class SendTextMessageToUserCommand(UserCommandBase):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    @abc.abstractmethod
    async def do_exec(self):
        await self.external.tg.reply_on_message(self.message, self.text)
