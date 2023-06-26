from external.db.models import User
from utrust.actions.app.message.base import MessageActionBase
from utrust.context import UserContext

from utrust.actions.permissions import Permission


class UserActionBase(MessageActionBase):
    def __init__(self, user_context: UserContext):
        super().__init__(user_context.message_context)

        self.user_context: UserContext = user_context
        self.permissions = [Permission.AUTHORIZED]

    @property
    def user(self) -> User:
        return self.user_context.user
