import tempfile
from pathlib import Path

from external.gcp import GCPFacade
from external.tg import TelegramFacade, Message
from utils.st import rand_string_id


class UTrustBot:
    def __init__(self, gcp: GCPFacade, tg: TelegramFacade):
        self.gcp = gcp
        self.tg = tg

        self.tmp_dir = Path(tempfile.mkdtemp(suffix='tg-audio-files'))

        self.tg.add_message_processor(self.receive_message)

    def run_polling(self):
        self.tg.run_polling()

    def run_webhook(self, *args):
        self.tg.run_webhook(*args)

    async def receive_message(self, msg: Message):
        dest = self.tmp_dir / rand_string_id(prefix='audio-', suffix='.ogg')

        audio_file = await msg.save_voice_file(dest)
        url = self.gcp.upload_to_bucket(audio_file)
        text = self.gcp.speech_to_text(url)
        await self.tg.send_text_message(msg, text)
