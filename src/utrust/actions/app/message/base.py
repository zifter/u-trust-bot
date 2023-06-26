from external.tg.message import Message
from utrust.actions.app.base import AppActionBase
from utrust.context import MessageContext


class MessageActionBase(AppActionBase):
    def __init__(self, message_context: MessageContext):
        super().__init__(message_context.app_context)

        self.message_context: MessageContext = message_context

    @property
    def message(self) -> Message:
        return self.message_context.message
