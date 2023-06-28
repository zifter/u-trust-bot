from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class DetermineUserTextRequestAction(UserActionBase):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    async def do_exec(self):
        return SendTextMessageToUserAction(self.text, self.user_context)
