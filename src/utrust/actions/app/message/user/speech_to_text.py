import abc

from utils.st import rand_string_id
from utrust.actions.app.message.user.base import UserActionBase
from utrust.actions.app.message.user.determine_user_text_request import DetermineUserTextRequestAction


class SpeechToTextAction(UserActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def do_exec(self):
        self.user.analytics.vo_total_seconds += self.message.vo_duration()

        audio_file_path = self.tmp_dir / rand_string_id(prefix=f'audio-{self.user.telegram_id}', suffix='.ogg')

        audio_file = await self.message.save_voice_file(audio_file_path)
        audio_url = self.external.gcp.upload_to_bucket(audio_file)
        text = self.external.gcp.speech_to_text(audio_url)

        return DetermineUserTextRequestAction(text, self.user_context)
