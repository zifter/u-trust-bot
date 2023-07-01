import pytest
from telegram import Message

from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


async def test_send_voice_message(user: UTrustUser):
    resp: Message = await user.command_info()

    assert "Joined:" in resp.text
    assert "Total Messages:" in resp.text
    assert "Total VO Duration:" in resp.text
