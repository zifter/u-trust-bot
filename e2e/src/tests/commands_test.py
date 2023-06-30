import pytest
from telegram import Message
from telethon.tl.custom import Conversation


pytestmark = [
    pytest.mark.e2e,
]


@pytest.mark.asyncio
async def test_command_my_lists(conv: Conversation):
    """Test /my_lists bot command."""
    await conv.send_message("/info")
    user_lists: Message = await conv.get_response()

    # Check that the message contains necessary text
    assert "Choose list or action" in user_lists.text
