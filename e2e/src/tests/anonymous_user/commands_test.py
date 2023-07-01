import pytest
from telegram import Message

from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


async def test_anonymous_command_info(user: UTrustUser):
    resp = await user.command_info()
    assert resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT
