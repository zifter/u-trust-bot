from shared.texts import TEXT_NO_ACTIVE_COMMAND, FORMAT_COMMAND_HAS_BEEN_CANCELLED
from utrust.actions.app.message.base import CommandStateMixin
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class CommandCancel(UserActionBase, CommandStateMixin):
    COMMAND_NAME = 'cancel'
    COMMAND_DESCR = 'cancel the current operation'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = []

    async def do_exec(self):
        current_command = self.command_name()
        if current_command == '':
            return SendTextMessageToUserAction(TEXT_NO_ACTIVE_COMMAND, self.user_context)
        else:
            self.command_complete()
            return SendTextMessageToUserAction(FORMAT_COMMAND_HAS_BEEN_CANCELLED(current_command), self.user_context)
