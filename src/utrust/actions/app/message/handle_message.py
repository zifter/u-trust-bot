from typing import Optional

from external.db.models import User
from external.tg.message import MessageContentType
from utrust.actions import logger
from utrust.actions.app.message.user.base import MessageActionBase
from utrust.actions.app.message.user.commands.command_cancel import CommandCancel
from utrust.actions.permissions import Permission
from utrust.actions.app.message.user.speech_to_text import SpeechToTextAction
from utrust.context import UserContext
from utrust.actions.app.message.user.commands.command_authorize_user import CommandAuthorizeUser


class HandleMessageAction(MessageActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user_context: Optional[UserContext] = None

    async def pre_exec(self):
        user = self.external.db.get_user(self.message.telegram_id)
        if user is None:
            user = self.external.db.create_new_user(self.message.telegram_id)

        user.analytics.processed_messages += 1

        self._user_context = UserContext(user, self.message_context)

    async def do_exec(self):
        action = self.get_next_action(self._user_context)

        if Permission.AUTHORIZED in action.permissions and not self._user_context.user.registration.confirmed:
            return CommandAuthorizeUser(self._user_context)

        return action

    async def post_exec(self, failed_to_exec=False):
        if self._user_context.user_delete_request:
            self.external.db.delete_user(self._user_context.user)
        else:
            self._user_context.user.analytics.failed_messages += 1 if failed_to_exec else 0
            self.external.db.save_user(self._user_context.user)

    def get_next_action(self, user_context: UserContext):
        command_name = self.message.command_name()
        if command_name and command_name == CommandCancel.COMMAND_NAME:
            action = self.app_context.commander.get_action_class(command_name)
            return action(user_context)

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
