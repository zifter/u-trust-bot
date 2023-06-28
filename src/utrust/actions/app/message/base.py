from abc import ABC

from external.tg.message import Message
from utrust.actions.app.base import AppActionBase
from utrust.context import MessageContext


class MessageActionBase(AppActionBase, ABC):
    def __init__(self, message_context: MessageContext):
        super().__init__(message_context.app_context)

        self.message_context: MessageContext = message_context

    @property
    def message(self) -> Message:
        return self.message_context.message


class CommandStateMixin:
    def command_complete(self):
        self.user.command_state.name = ''
        self.user.command_state.state = {}

    def command_state(self):
        state = self.user.command_state.state
        return state if state else {}

    def set_command_state(self, state):
        self.user.command_state.name = self.COMMAND_NAME
        self.user.command_state.state = state
