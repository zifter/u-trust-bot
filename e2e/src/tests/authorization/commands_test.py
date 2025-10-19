import pytest
import pytest_asyncio

from shared.texts import TEXT_YOU_ARE_NOT_AUTHORIZED, AUTHORIZATION_TOKEN, TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED, \
    TEXT_YOU_ACCOUNT_IS_DELETED, TEXT_WRONG_AUTH_TOKEN, FORMAT_COMMAND_HAS_BEEN_CANCELLED
from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


@pytest.mark.asyncio(loop_scope="session")
async def test_command_auth(user: UTrustUser):
    resp = await user.command_auth()

    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED

    resp = await user.send_text_message_ang_get_response("wrong token")
    assert resp.text == TEXT_WRONG_AUTH_TOKEN

    resp = await user.send_text_message_ang_get_response("wrong token 2")
    assert resp.text == TEXT_WRONG_AUTH_TOKEN

    resp = await user.send_text_message_ang_get_response(AUTHORIZATION_TOKEN)
    assert resp.text == TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_command_auth_cancel(user: UTrustUser):
    resp = await user.command_auth()

    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED

    resp = await user.command_cancel()
    assert resp.text == FORMAT_COMMAND_HAS_BEEN_CANCELLED('auth')

    resp = await user.command_info()
    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_command_forget_me(user: UTrustUser):
    resp = await user.command_auth()
    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED

    resp = await user.send_text_message_ang_get_response(AUTHORIZATION_TOKEN)
    assert resp.text == TEXT_THANKS_YOU_ARE_NOW_AUTHORIZED

    resp = await user.command_info()
    assert "Joined:" in resp.text

    resp = await user.command_forget_me()
    assert resp.text == TEXT_YOU_ACCOUNT_IS_DELETED

    resp = await user.command_info()
    assert resp.text == TEXT_YOU_ARE_NOT_AUTHORIZED
