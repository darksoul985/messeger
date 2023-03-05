import logging
"""Константы"""

# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
TEXT_MESSAGE = 'text_message'
SENDER = 'sender'
DESTINATION = 'to'


# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
MESSAGE = 'message'
RESPONSE = 'response'
ERROR = 'error'
EXIT = 'exit'


# Параметры запуска сервера
SHORT_ADDRESS_ARGS = 'a'
ADDRESS_ARGS = 'address'
SHORT_PORT_ARGS = 'p'
PORT_ARGS = 'port'

# уровень логирования
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

level = 'debug'

LOGGING_LEVEL = LEVELS.get(level, logging.NOTSET)

# таймаут опроса
TIMEOUT_STEP= 0.2


# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
