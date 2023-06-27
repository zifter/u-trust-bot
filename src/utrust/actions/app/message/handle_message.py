from typing import Optional

from external.db.models import User
from external.tg.message import MessageContentType
from utrust.actions import logger
from utrust.actions.app.message.user.base import MessageActionBase
from utrust.actions.permissions import Permission
from utrust.actions.app.message.user.speech_to_text import SpeechToTextAction
from utrust.context import UserContext
from utrust.actions.app.message.user.commands.command_authorize_user import CommandAuthorizeUser


class HandleMessageAction(MessageActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user: Optional[User] = None

    async def pre_exec(self):
        self._user = self.external.db.get_user(self.message.telegram_id)
        if self._user is None:
            self._user = self.external.db.create_new_user(self.message.telegram_id)

        self._user.analytics.processed_messages += 1

    async def do_exec(self):
        user_context = UserContext(self._user, self.message_context)

        action = self.get_next_action(user_context)

        try:
            if Permission.AUTHORIZED in action.permissions and not self._user.registration.confirmed:
                return CommandAuthorizeUser(user_context)

            return action
        finally:
            self._user.analytics.failed_messages += 1

    async def post_exec(self, failed_to_exec=False):
        self._user.analytics.failed_messages += 1 if failed_to_exec else 0
        self.external.db.save_user(self._user)

    def get_next_action(self, user_context: UserContext):
        if user_context.user.command_state.name:
            action = self.app_context.commander.get_action_class(user_context.user.command_state.name)
            return action(user_context)

        if self.message.content_type == MessageContentType.COMMAND:
            args = self.message.text.split(' ')
            command_name = args[0][1:]

            # TODO Unknown command exception
            action = self.app_context.commander.get_action_class(command_name)
            return action(user_context)
        elif self.message.content_type == MessageContentType.TEXT:
            pass
        elif self.message.content_type == MessageContentType.VOICE:
            return SpeechToTextAction(user_context)
        else:
            raise RuntimeError(f'Unknown message content type {self.message.content_type}')
