import pickle
from dataclasses import dataclass

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from external.tg.callback_data import CallbackData
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.send_text_message_to_user import SendTextMessageToUserAction


class DetermineUserTextRequestAction(UserActionBase):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

    async def do_exec(self):
        callback_data = CallbackData('complete_task', {})

        button = InlineKeyboardButton("Complete", callback_data=callback_data.serialize())
        reply_markup = InlineKeyboardMarkup([[button]])

        return SendTextMessageToUserAction(self.text, self.user_context, reply_markup=reply_markup)
