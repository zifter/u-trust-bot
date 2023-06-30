import asyncio

import pytest

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom import Conversation

from settings import TELEGRAM_APP_SESSION, TELEGRAM_APP_ID, TELEGRAM_APP_HASH, TEST_BOT_NAME


# Default event_loop fixture has "function" scope and will
# through ScopeMismatch exception since there are related
# fixtures with "session" scope. Need to override to set scope.
# https://github.com/pytest-dev/pytest-asyncio#event_loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def telegram_client():
    """Connect to Telegram user for testing."""
    assert TELEGRAM_APP_SESSION
    assert TELEGRAM_APP_ID
    assert TELEGRAM_APP_HASH

    async with TelegramClient(StringSession(TELEGRAM_APP_SESSION), TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as client:
        yield client


@pytest.fixture(scope="session")
async def conv(telegram_client) -> Conversation:
    """Open conversation with the bot."""
    async with telegram_client.conversation(TEST_BOT_NAME, timeout=10, max_messages=10000) as conv:
        conv: Conversation
        await conv.send_message("/start")
        _ = await conv.get_response()  # Welcome message
        await conv.send_message("/auth")
        auth = await conv.get_response()
        if 'Please, send me authorization code' in auth.text:
            await conv.send_message("I-trust-U")
        elif 'You are already authorized' in auth.text:
            pass
        else:
            assert False, 'Unknown state'

        yield conv
