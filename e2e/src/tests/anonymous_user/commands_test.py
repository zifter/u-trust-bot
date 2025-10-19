import pytest

from shared.texts import TEXT_YOU_ARE_NOT_AUTHORIZED
from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


@pytest.mark.asyncio(loop_scope="session")
async def test_anonymous_command_info(user: UTrustUser):
    resp = await user.command_info()
    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED
