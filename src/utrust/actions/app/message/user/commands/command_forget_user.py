from utrust.actions.app.message.base import CommandStateMixin
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class CommandForgetUser(UserActionBase, CommandStateMixin):
    COMMAND_NAME = 'forgetme'
    COMMAND_DESCR = 'Delete all data that bot aware about you'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = []

    async def do_exec(self):
        self.user_context.user = self.external.db.create_new_user(self.user.telegram_id)
        self.command_complete()

        return SendTextMessageToUserAction('You account is deleted', self.user_context)
