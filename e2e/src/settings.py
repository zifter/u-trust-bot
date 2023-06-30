import os
from pathlib import Path

WORKING_DIR = Path(__file__).parent.parent
TEST_DATA_DIR = WORKING_DIR / 'testdata'

TELEGRAM_APP_ID = int(os.environ.get("TELEGRAM_APP_ID", -1))
TELEGRAM_APP_HASH = os.environ.get("TELEGRAM_APP_HASH")
TELEGRAM_APP_SESSION = os.environ.get("TELEGRAM_APP_SESSION")

TEST_BOT_NAME = os.environ.get("UTRUST_BOT_NAME")
