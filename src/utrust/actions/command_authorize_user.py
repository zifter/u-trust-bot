from utrust.actions.base import UserActionBase
from utrust.actions.send_text_message_to_user import SendTextMessageToUserAction


class CommandAuthorizeUser(UserActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        return SendTextMessageToUserAction('You are not authorized', self.user_context)
