import logging
from pathlib import Path

from google.cloud import storage
from google.cloud import speech

logger = logging.getLogger('gcp')


class GCPFacade:
    def __init__(self, speech_to_text_workspace, lang):
        self.storage_client = storage.Client()
        self.speech_client = speech.SpeechClient()
        self.speech_workspace = speech_to_text_workspace
        self.lang = lang

    def upload_to_bucket(self, audio_file: Path) -> str:
        logger.info(f'Upload to bucket {audio_file}')

        return self._upload_blob(self.speech_workspace, audio_file, 'audio-files/' + audio_file.name)

    def speech_to_text(self, url_bucket) -> str:
        logger.info(f'Speech to text {url_bucket}')

        audio = speech.RecognitionAudio(uri=url_bucket)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code=self.lang,
            model="default",
            audio_channel_count=1,
            enable_word_time_offsets=True,
        )

        # Detects speech in the audio file
        operation = self.speech_client.long_running_recognize(config=config, audio=audio)

        logger.info("Waiting for operation to complete...")
        response = operation.result(timeout=5*60)

        transcripts = []
        for result in response.results:
            for alternative in result.alternatives:
                transcripts.append(alternative.transcript)

        return transcripts[0]

    def _upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        result = blob.upload_from_filename(source_file_name)

        logger.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

        return f'gs://{bucket_name}/{destination_blob_name}'
