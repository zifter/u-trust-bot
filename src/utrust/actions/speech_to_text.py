import abc

from utils.st import rand_string_id
from utrust.actions.base import UserActionBase
from utrust.actions.send_text_message_to_user import SendTextMessageToUserAction


class SpeechToTextAction(UserActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    async def do_exec(self):
        self.user.analytics.vo_total_seconds += self.message.vo_duration()

        audio_file_path = self.tmp_dir / rand_string_id(prefix='audio-', suffix='.ogg')

        audio_file = await self.message.save_voice_file(audio_file_path)
        audio_url = self.external.gcp.upload_to_bucket(audio_file)
        text = self.external.gcp.speech_to_text(audio_url)

        return SendTextMessageToUserAction(text, self.user_context)
