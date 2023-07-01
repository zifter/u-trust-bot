import pytest
from telegram import Message

from settings import TEST_DATA_DIR
from utrustuser import UTrustUser


pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


async def test_send_voice_message(user: UTrustUser):
    test_file = TEST_DATA_DIR / 'audio' / 'audio_call_mama.ogg'
    resp: Message = await user.send_file_message_ang_get_response(test_file)
    assert resp.text == 'позвонить маме купить хлеб'
