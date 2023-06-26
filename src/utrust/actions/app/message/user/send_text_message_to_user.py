import abc

from utrust.actions.app.message.user.base import UserActionBase


class SendTextMessageToUserAction(UserActionBase):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    @abc.abstractmethod
    async def do_exec(self):
        await self.external.tg.reply_on_message(self.message, self.text)
