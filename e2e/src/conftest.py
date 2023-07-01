import asyncio

import pytest

from telethon import TelegramClient
from telethon.sessions import StringSession

from settings import TELEGRAM_APP_SESSION, TELEGRAM_APP_ID, TELEGRAM_APP_HASH


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
