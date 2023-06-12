import tempfile
from pathlib import Path

from external.storage import User
from external.tg import Message
from external.facade import ExternalAPIFacade


class AppContext:
    def __init__(self, facade: ExternalAPIFacade):
        self.external = facade
        self.tmp_dir = Path(tempfile.mkdtemp(suffix='app-temp'))


class MessageContext:
    def __init__(self, message: Message, app_context: AppContext):
        self.app_context = app_context

        self.message = message


class UserCommandContext:
    def __init__(self, user: User, message_context: MessageContext):
        self.message_context = message_context

        self.user = user

