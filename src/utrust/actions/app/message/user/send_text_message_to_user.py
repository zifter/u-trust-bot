from utrust.actions.app.message.user.base import UserActionBase


class SendTextMessageToUserAction(UserActionBase):
    def __init__(self, text, *args, reply_markup=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text
        self.reply_markup = reply_markup

    async def do_exec(self):
        await self.external.tg.reply_on_message(self.message, self.text, reply_markup=self.reply_markup)


