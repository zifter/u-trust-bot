import tempfile
from pathlib import Path

from external.db.models import User
from external.tg.message import Message
from external import ExternalAPI
from utrust.commander import Commander


class AppContext:
    def __init__(self, ext: ExternalAPI, commander: Commander):
        self.external = ext
        self.commander = commander
        self.tmp_dir = Path(tempfile.mkdtemp(suffix='app-temp'))


class MessageContext:
    def __init__(self, message: Message, app_context: AppContext):
        self.app_context = app_context

        self.message = message


class UserContext:
    def __init__(self, user: User, message_context: MessageContext):
        self.message_context = message_context

        self.user = user
        self.user_delete_request: bool = False

    def request_user_deletion(self):
        self.user_delete_request = True
