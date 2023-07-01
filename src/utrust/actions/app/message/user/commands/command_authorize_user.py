from utrust.actions.app.message.base import CommandStateMixin
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class CommandAuthorizeUser(UserActionBase, CommandStateMixin):
    COMMAND_NAME = 'auth'
    COMMAND_DESCR = 'Authorize to use full functions'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = []

    async def do_exec(self):
        if self.user.registration.confirmed:
            self.command_complete()
            return SendTextMessageToUserAction(f'You are already authorized', self.user_context)

        # /auth -> Message
        # TOKEN -> Message
        waiting_token = self.command_state().get('waiting_token', False)
        if waiting_token:
            if self.message.text == 'I-trust-U':
                self.command_complete()
                self.user.registration.confirmed = True
                return SendTextMessageToUserAction('Thanks! You are authorized to work with me', self.user_context)
            else:
                return SendTextMessageToUserAction(f'Wrong auth token. Please, send me authorization code', self.user_context)
        else:
            self.set_command_state({'waiting_token': True})
            return SendTextMessageToUserAction('You are not authorized. Please, send me authorization code', self.user_context)
