import tempfile
from pathlib import Path

from external.gcp import GCPFacade
from external.storage import Storage, User
from external.tg import TelegramFacade, Message
from utils.st import rand_string_id


class UTrustBot:
    def __init__(self, gcp: GCPFacade, tg: TelegramFacade, db: Storage):
        self.gcp = gcp
        self.tg = tg
        self.db = db

        self.tmp_dir = Path(tempfile.mkdtemp(suffix='tg-audio-files'))

        self.tg.add_message_processor(self.process_message)

    def run_polling(self):
        self.tg.run_polling()

    def run_webhook(self, *args):
        self.tg.run_webhook(*args)

    async def process_message(self, msg: Message):
        audio_file_path = self.tmp_dir / rand_string_id(prefix='audio-', suffix='.ogg')

        user: User = self.db.get_user(msg.telegram_id)
        if user is None:
            user = User()
            user.telegram_id = msg.telegram_id
            self.db.create_user(user)

        audio_file = await msg.save_voice_file(audio_file_path)
        audio_url = self.gcp.upload_to_bucket(audio_file)
        text = self.gcp.speech_to_text(audio_url)
        await self.tg.reply_on_message(msg, text)
