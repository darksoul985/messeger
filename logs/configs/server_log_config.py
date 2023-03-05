import sys
import os
import logging
import logging.handlers
import pathlib
sys.path.append(os.path.join(os.getcwd(), '../..'))
from common.variables import LOGGING_LEVEL


# путь для файла логирования
# TODO дописать создание директории с логами если нет
if 'logs' in str(pathlib.Path(__file__)):
    for i in pathlib.Path(__file__).parents:
        if i.name == 'logs':
            PATH = pathlib.Path(i).joinpath('log_files', 'server.log')

else:
    PATH = pathlib.Path(__file__).parent.joinpath('server.log')

# создаем логгер
SERVER_LOGER = logging.getLogger('server')

# задаем уровень логирования из переменных приложения
SERVER_LOGER.setLevel(LOGGING_LEVEL)

# задаем файл логирования
LOG_FILE = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf-8', interval=1, when='D'
)

# задаем форматирование записей логов
# <дата-время> <уровень важности> <имя модуля> <сообщение>
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
)

# присваиваем формат обработчику
LOG_FILE.setFormatter(formatter)

# добавляем обработчик в логгер и запускаем
SERVER_LOGER.addHandler(LOG_FILE)
SERVER_LOGER.setLevel(LOGGING_LEVEL)


def main():
    """отладка"""
    SERVER_LOGER.critical('Критическая ошибка')
    SERVER_LOGER.error('Ошибка')
    SERVER_LOGER.debug('Отладочная информация')
    SERVER_LOGER.info('Информационное сообщение')


if __name__ == '__main__':
    main()
