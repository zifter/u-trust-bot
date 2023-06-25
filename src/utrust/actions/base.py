import abc
from pathlib import Path
from typing import final, Optional, List

from external.db.models import User
from external.facade import ExternalAPIFacade
from external.tg import Message
from utrust.context import AppContext, MessageContext, UserContext

from . import logger
from .permissions import Permission


class ActionBase:
    def __init__(self):
        self.permissions = []

    @final
    async def exec(self):
        logger.info(f'Execute {self.__class__}. Start')

        commands = await self.do_exec()
        if commands:
            if isinstance(commands, ActionBase):
                await commands.exec()
            elif isinstance(commands, list):
                for cmd in commands:
                    await cmd.exec()
            else:
                raise ValueError()

        logger.info(f'Execute {self.__class__.__name__}. End')

    @abc.abstractmethod
    async def do_exec(self) -> Optional[List['ActionBase']]:
        raise NotImplemented()


class AppActionBase(ActionBase):
    def __init__(self, app_context: AppContext):
        super().__init__()

        self.app_context = app_context

    @property
    def external(self) -> ExternalAPIFacade:
        return self.app_context.external

    @property
    def tmp_dir(self) -> Path:
        return self.app_context.tmp_dir


class MessageActionBase(AppActionBase):
    def __init__(self, message_context: MessageContext):
        super().__init__(message_context.app_context)

        self.message_context: MessageContext = message_context

    @property
    def message(self) -> Message:
        return self.message_context.message


class UserActionBase(MessageActionBase):
    def __init__(self, user_context: UserContext):
        super().__init__(user_context.message_context)

        self.user_context: UserContext = user_context
        self.permissions = [Permission.AUTHORIZED]

    @property
    def user(self) -> User:
        return self.user_context.user
