import logging
import sys
import os
from pythonjsonlogger import jsonlogger


def setup_json_logger(name: str = 'u-trust-bot', level: int = None):
    """
    Настраивает глобальный логгер для вывода в JSON формате

    Args:
        name: имя логгера
        level: уровень логирования (если None, берется из переменной окружения UTRUST_LOG_LEVEL или INFO)
    """
    # Определяем уровень логирования
    if level is None:
        log_level_str = os.environ.get('UTRUST_LOG_LEVEL', 'INFO').upper()
        level = getattr(logging, log_level_str, logging.INFO)

    # Создаем форматтер для JSON
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Настраиваем handler для stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(json_formatter)

    # Получаем root logger и настраиваем его
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()  # Очищаем существующие handlers
    root_logger.addHandler(handler)

    # Настраиваем основной логгер приложения
    app_logger = logging.getLogger(name)
    app_logger.setLevel(level)

    return app_logger
