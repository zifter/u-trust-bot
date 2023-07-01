import pytest
from telegram import Message
from telethon.tl.custom import Conversation

from utrustuser import UTrustUser

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.asyncio,
]


async def test_command_auth(user: UTrustUser):
    resp = await user.command_auth()

    assert resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT

    resp = await user.send_text_message_ang_get_response("wrong token")
    assert resp.text == UTrustUser.WRONG_AUTH_TOKEN_TEXT

    resp = await user.send_text_message_ang_get_response("wrong token 2")
    assert resp.text == UTrustUser.WRONG_AUTH_TOKEN_TEXT

    resp = await user.send_text_message_ang_get_response("wrong token 2")
    assert resp.text == UTrustUser.WRONG_AUTH_TOKEN_TEXT

    resp = await user.send_text_message_ang_get_response(UTrustUser.AUTHORIZATION_TOKEN)
    assert resp.text == UTrustUser.AUTHORIZED_CONGRATULATIONS_TEXT


async def test_command_auth_cancel(user: UTrustUser):
    resp = await user.command_auth()

    assert resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT

    resp = await user.command_cancel()
    assert user.is_canceled_text(resp.text, 'auth'), resp.text

    resp = await user.command_info()
    assert user.is_not_autorized_text(resp.text), resp.text


async def test_command_forget_me(user: UTrustUser):
    resp = await user.command_auth()
    assert resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT

    resp = await user.send_text_message_ang_get_response(UTrustUser.AUTHORIZATION_TOKEN)
    assert resp.text == UTrustUser.AUTHORIZED_CONGRATULATIONS_TEXT

    resp = await user.command_info()
    assert "Joined:" in resp.text

    resp = await user.command_forget_me()
    assert resp.text == UTrustUser.YOU_ACCOUNT_IS_DELETED_TEXT

    resp = await user.command_info()
    assert resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT
