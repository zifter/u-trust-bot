from shared.texts import TEXT_YOU_ARE_NOT_AUTHORIZED, TEXT_WRONG_AUTH_TOKEN, TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED, \
    TEXT_YOU_ARE_ALREADY_AUTHORIZED, AUTHORIZATION_TOKEN
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
            return SendTextMessageToUserAction(TEXT_YOU_ARE_ALREADY_AUTHORIZED, self.user_context)

        # /auth -> Message
        # TOKEN -> Message
        waiting_token = self.command_state().get('waiting_token', False)
        if waiting_token:
            if self.message.text == AUTHORIZATION_TOKEN:
                self.command_complete()
                self.user.registration.confirmed = True
                return SendTextMessageToUserAction(TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED, self.user_context)
            else:
                return SendTextMessageToUserAction(TEXT_WRONG_AUTH_TOKEN, self.user_context)
        else:
            self.set_command_state({'waiting_token': True})

            return SendTextMessageToUserAction(TEXT_YOU_ARE_NOT_AUTHORIZED, self.user_context)
