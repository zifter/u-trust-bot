from utrust.actions.app.message.base import CommandStateMixin
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class CommandStart(UserActionBase, CommandStateMixin):
    COMMAND_NAME = 'start'
    COMMAND_DESCR = 'Show welcome message'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = []

    async def do_exec(self):
        self.command_complete()
        return SendTextMessageToUserAction(self.app_context.commander.help_description(), self.user_context)
