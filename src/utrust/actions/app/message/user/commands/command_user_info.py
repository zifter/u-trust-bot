from utils.st import format_duration
from utrust.actions.app.message.base import CommandStateMixin
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class CommandUserInfo(UserActionBase, CommandStateMixin):
    COMMAND_NAME = 'info'
    COMMAND_DESCR = 'Show account info'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        self.command_complete()

        message = \
            f'Joined:  {self.user.registration.created_at.strftime("%H:%M, %A, %B %d, %Y")}\n' \
            f'Total Messages:  {self.user.analytics.processed_messages}\n' \
            f'Total VO Duration:  {format_duration(self.user.analytics.vo_total_seconds)}\n'

        return SendTextMessageToUserAction(message, self.user_context)
