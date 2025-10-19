import pytest
import pytest_asyncio
from telegram import Message

from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


@pytest.mark.asyncio(loop_scope="session")
async def test_send_voice_message(user: UTrustUser):
    resp: Message = await user.command_info()

    assert "Joined:" in resp.text
    assert "Total Messages:" in resp.text
    assert "Total Transcription Duration:" in resp.text
