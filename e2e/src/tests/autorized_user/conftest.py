import pytest

from settings import TEST_BOT_NAME
from utrustuser import UTrustUser


@pytest.fixture(scope="module")
async def user(telegram_client) -> UTrustUser:
    """Open conversation with the bot."""
    async with telegram_client.conversation(TEST_BOT_NAME, timeout=30, max_messages=10000) as conv:
        user = UTrustUser(conv)
        await user.command_start()
        await user.authorize()

        yield user

        await user.delete_conversation()
