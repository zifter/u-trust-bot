import os
from argparse import ArgumentParser

from external.gcp import GCPFacade
from external.tg import TelegramFacade
from utrust.bot import UTrustBot


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--telegram-token", default=os.environ.get('UTRUST_TELEGRAM_TOKEN', None))
    parser.add_argument("--speech-to-text-workspace", default=os.environ.get('UTRUST_SPEECH_TO_TEXT_WORKSPACE', None))
    return parser.parse_args()


def main(telegram_token: str, speech_to_text_workspace):
    gcp = GCPFacade(speech_to_text_workspace)
    tg = TelegramFacade(telegram_token)

    UTrustBot(gcp, tg).process()


if __name__ == '__main__':
    args = get_args()
    main(**vars(args))
