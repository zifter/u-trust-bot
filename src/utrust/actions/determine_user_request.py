from external.tg import MessageContentType
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction
from utrust.actions.app.message.user.speech_to_text import SpeechToTextAction
from utrust.actions.app.message.user.commands.command_forget_user import CommandForgetUser

from utrust.actions.app.message.user.base import UserActionBase


class DetermineUserRequestAction(UserActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        if self.message.content_type == MessageContentType.COMMAND:
            command = self.message.text.split(' ')[0]
            if command == '/start':
                return SendTextMessageToUserAction('My help for you.', self.user_context)
            elif command == '/deleteaccount':
                return CommandForgetUser(self.user_context)
        elif self.message.content_type == MessageContentType.TEXT:
            pass
        elif self.message.content_type == MessageContentType.VOICE:
            return SpeechToTextAction(self.user_context)
        else:
            raise RuntimeError(f'Unknown message content type {self.message.content_type}')
