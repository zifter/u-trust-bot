import pytest
from telegram import Message
from telethon.tl.custom import Conversation


pytestmark = [
    pytest.mark.e2e,
]


@pytest.mark.asyncio
async def test_command_info(conv: Conversation):
    """Test /my_lists bot command."""
    await conv.send_message("/info")
    info: Message = await conv.get_response()

    # Check that the message contains necessary text
    assert "Joined:" in info.text
    assert "Total Messages:" in info.text
    assert "Total VO Duration:" in info.text
