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
            PATH = pathlib.Path(i).joinpath('log_files', 'client.log')

else:
    PATH = pathlib.Path(__file__).parent.joinpath('client.log')

# создаем логгер
CLIENT_LOGER = logging.getLogger('client')

# задаем уровень логирования из переменных приложения
CLIENT_LOGER.setLevel(LOGGING_LEVEL)

# задаем файл логирования
LOG_FILE = logging.FileHandler(PATH, encoding='utf-8')

# задаем форматирование записей логов
# <дата-время> <уровень важности> <имя модуля> <сообщение>
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
)

# присваиваем формат обработчику
LOG_FILE.setFormatter(formatter)

# добавляем обработчик в логгер и запускаем
CLIENT_LOGER.addHandler(LOG_FILE)
CLIENT_LOGER.setLevel(LOGGING_LEVEL)


def main():
    """отладка"""
    CLIENT_LOGER.critical('Критическая ошибка')
    CLIENT_LOGER.error('Ошибка')
    CLIENT_LOGER.debug('Отладочная информация')
    CLIENT_LOGER.info('Информационное сообщение')


if __name__ == '__main__':
    main()
