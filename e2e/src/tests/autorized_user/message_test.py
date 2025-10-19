import pytest
import pytest_asyncio
from telegram import Message

from settings import TEST_DATA_DIR
from utrustuser import UTrustUser


pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


@pytest.mark.asyncio(loop_scope="session")
async def test_send_voice_message(user: UTrustUser):
    test_file = TEST_DATA_DIR / 'audio' / 'audio_call_mama.ogg'
    resp: Message = await user.send_file_message_ang_get_response(test_file)
    assert resp.text == 'Позвонить маме купить хлеб.'
