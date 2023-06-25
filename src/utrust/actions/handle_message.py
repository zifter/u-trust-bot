from external.db.models import User
from external.tg import MessageContentType
from utrust.actions.base import MessageActionBase
from utrust.actions.permissions import Permission
from utrust.actions.speech_to_text import SpeechToTextAction
from utrust.context import UserContext
from utrust.actions.command_authorize_user import CommandAuthorizeUser


class HandleMessageAction(MessageActionBase):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = commands

    async def do_exec(self):
        user: User = self.external.db.get_user(self.message.telegram_id)
        if user is None:
            user = self.external.db.create_new_user(self.message.telegram_id)
            self.external.db.save_user(user)

        user.analytics.processed_messages += 1

        user_context = UserContext(user, self.message_context)

        action = self.get_next_action(user_context)

        try:
            if Permission.AUTHORIZED in action.permissions and not user.registration.confirmed:
                return CommandAuthorizeUser(user_context)

            return action
        finally:
            user.analytics.failed_messages += 1

            self.external.db.save_user(user)

    def get_next_action(self, user_context: UserContext):
        if self.message.content_type == MessageContentType.COMMAND:
            args = self.message.text.split(' ')
            command_name = args[0][1:]
            for name, descr, action in self.commands:
                if name == command_name:
                    return action(user_context)
        elif self.message.content_type == MessageContentType.TEXT:
            pass
        elif self.message.content_type == MessageContentType.VOICE:
            return SpeechToTextAction(user_context)
        else:
            raise RuntimeError(f'Unknown message content type {self.message.content_type}')
