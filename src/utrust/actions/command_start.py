from utrust.actions.base import UserActionBase
from utrust.actions.send_text_message_to_user import SendTextMessageToUserAction


class CommandStart(UserActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissions = []

    async def do_exec(self):
        return SendTextMessageToUserAction('Full descriptions', self.user_context)
