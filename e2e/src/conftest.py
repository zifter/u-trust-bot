import asyncio
import sys
import os

import pytest_asyncio

from telethon import TelegramClient, helpers
from telethon.sessions import StringSession

from settings import TELEGRAM_APP_SESSION, TELEGRAM_APP_ID, TELEGRAM_APP_HASH


@pytest_asyncio.fixture(loop_scope="session")
async def telegram_client():
    """Connect to Telegram user for testing."""
    assert TELEGRAM_APP_SESSION, "TELEGRAM_APP_SESSION environment variable is required"
    assert TELEGRAM_APP_ID, "TELEGRAM_APP_ID environment variable is required"
    assert TELEGRAM_APP_HASH, "TELEGRAM_APP_HASH environment variable is required"

    # Проверяем, что сессия не пустая
    if not TELEGRAM_APP_SESSION.strip():
        raise RuntimeError(
            "TELEGRAM_APP_SESSION is empty. Please run telegram_first_login_init.py to create a new session."
        )

    # Перенаправляем stdin на /dev/null для предотвращения интерактивных запросов
    original_stdin = sys.stdin
    if os.path.exists('/dev/null'):
        sys.stdin = open('/dev/null', 'r')

    try:
        client = TelegramClient(
            StringSession(TELEGRAM_APP_SESSION),
            TELEGRAM_APP_ID,
            TELEGRAM_APP_HASH,
            auto_reconnect=False,
            use_ipv6=False,
            system_version="4.16.30-vxCUSTOM",
        )

        # Проверяем подключение
        await client.connect()

        if not await client.is_user_authorized():
            await client.disconnect()
            raise RuntimeError(
                "Telegram session is not authorized. Please regenerate TELEGRAM_APP_SESSION. "
                "Run telegram_first_login_init.py to create a new session."
            )

        try:
            yield client
        finally:
            if client.is_connected():
                await client.disconnect()

    finally:
        # Восстанавливаем original stdin
        sys.stdin = original_stdin
