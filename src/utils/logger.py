import logging


def get_logger(name: str) -> logging.Logger:
    # Создаём именованный логгер.
    logger = logging.getLogger(name)

    # Настраиваем только один раз.
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Вывод логов в стандартный поток.
        handler = logging.StreamHandler()

        # Формат сообщения.
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger
