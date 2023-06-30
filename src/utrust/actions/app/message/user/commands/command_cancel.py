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
            txt = "No active command to cancel. I wasn't doing anything anyway. Zzzzz..."
            return SendTextMessageToUserAction(txt, self.user_context)
        else:
            txt = f"The command {current_command} has been cancelled. Anything else I can do for you?\n\n" \
                  "Send /help for a list of commands. "
            self.command_complete()
            return SendTextMessageToUserAction(txt, self.user_context)
