import logging
import os

from argparse import ArgumentParser

from google.cloud import ndb

from external.gcp import GCP
from external.db.storage import Storage
from external.tg import Telegram
from external.facade import ExternalAPIFacade

from utrust.bot import BotApplication


logger = logging.getLogger('u-trust-bot')


def env_var(env, default=None, prefix='UTRUST_'):
    return os.environ.get(f'{prefix}{env}', default)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--environment-name", default=env_var('ENVIRONMENT_NAME', 'test'), type=str)
    parser.add_argument("--telegram-token", default=env_var('TELEGRAM_TOKEN', None))
    parser.add_argument("--speech-to-text-workspace", default=env_var('SPEECH_TO_TEXT_WORKSPACE', None))
    parser.add_argument("--language", default=env_var('LANGUAGE', "ru-RU"), type=str)

    subparsers = parser.add_subparsers(dest='command')

    parser_handler = subparsers.add_parser('polling', help='Run Telegram MessageHandler')
    parser_handler.set_defaults(command_func=cmd_polling)

    parser_handler = subparsers.add_parser('webhook', help='Run Telegram MessageHandler')
    parser_handler.add_argument("--secret-token", default=env_var('SECRET_TOKEN', None), type=str)
    parser_handler.add_argument("--url", default=env_var('URL', None), type=str)
    parser_handler.add_argument("--port", default=int(env_var('PORT', 8080)), type=int)
    parser_handler.set_defaults(command_func=cmd_webhook)

    parser_init = subparsers.add_parser('app-migrate', help='Migration Application State')
    parser_init.set_defaults(command_func=cmd_app_migrate)

    return parser.parse_args()


def cmd_polling(app: BotApplication):
    app.run_polling()


def cmd_webhook(app: BotApplication, port: int, secret_token: str, url: str):
    app.run_webhook(port, secret_token, url)


def cmd_app_migrate(app: BotApplication):
    app.app_migrate()


def main(command_func,
         command: str,
         environment_name: str,
         telegram_token: str,
         speech_to_text_workspace: str,
         language: str,
         **kwargs):
    logger.info(f'Start bot with command {command}')

    external = ExternalAPIFacade(
        gcp=GCP(speech_to_text_workspace, language),
        tg=Telegram(telegram_token),
        db=Storage(ndb.Client(namespace=environment_name))
    )
    bot = BotApplication(external)
    command_func(bot, **kwargs)


if __name__ == '__main__':
    args = get_args()
    logger.info(args)

    cmd = args.command

    main(**vars(args))
