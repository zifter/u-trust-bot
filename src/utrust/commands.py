import abc
from logging import getLogger
from pathlib import Path
from typing import final, Optional, List

from external.facade import ExternalAPIFacade
from external.storage import User
from external.tg import Message
from utils.st import rand_string_id

from utrust.context import MessageContext, UserCommandContext, AppContext

logger = getLogger('commands')


class Command:
    def __init__(self):
        pass

    @final
    async def exec(self):
        logger.info(f'Execute {self.__class__}. Start')

        commands = await self.do_exec()
        if commands:
            if isinstance(commands, Command):
                await commands.exec()
            elif isinstance(commands, list):
                for cmd in commands:
                    await cmd.exec()
            else:
                raise ValueError()

        logger.info(f'Execute {self.__class__}. End')

    @abc.abstractmethod
    async def do_exec(self) -> Optional[List['Command']]:
        raise NotImplemented()


class AppCommand(Command):
    def __init__(self, app_context: AppContext):
        super().__init__()

        self.app_context = app_context

    @property
    def external(self) -> ExternalAPIFacade:
        return self.app_context.external

    @property
    def tmp_dir(self) -> Path:
        return self.app_context.tmp_dir


class MessageCommand(AppCommand):
    def __init__(self, message_context: MessageContext):
        super().__init__(message_context.app_context)

        self.message_context: MessageContext = message_context

    @property
    def message(self) -> Message:
        return self.message_context.message


class UserCommand(MessageCommand):
    def __init__(self, user_context: UserCommandContext):
        super().__init__(user_context.message_context)

        self.user_context: UserCommandContext = user_context

    @property
    def user(self) -> User:
        return self.user_context.user


class ProcessMessageCommand(MessageCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        user: User = self.external.db.get_user(self.message.telegram_id)
        if user is None:
            user = User()
            user.telegram_id = self.message.telegram_id
            self.external.db.create_user(user)

        user_context = UserCommandContext(user, self.message_context)

        return [
            AuthorizeUserCommand(user_context),
            SpeechToTextCommand(user_context),
        ]


class AuthorizeUserCommand(UserCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    async def do_exec(self):
        pass


class SpeechToTextCommand(UserCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    async def do_exec(self):
        audio_file_path = self.tmp_dir / rand_string_id(prefix='audio-', suffix='.ogg')

        audio_file = await self.message.save_voice_file(audio_file_path)
        audio_url = self.external.gcp.upload_to_bucket(audio_file)
        text = self.external.gcp.speech_to_text(audio_url)

        return SendTextMessageToUserCommand(text, self.user_context)


class SendTextMessageToUserCommand(UserCommand):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    @abc.abstractmethod
    async def do_exec(self):
        await self.external.tg.reply_on_message(self.message, self.text)
