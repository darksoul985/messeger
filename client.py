"""Программа-клиент"""

import socket
import sys
import argparse
import threading
import json
import time
import logging
import logs.configs.client_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, ADDRESS_ARGS, \
    PORT_ARGS, MESSAGE, TEXT_MESSAGE, SENDER, DESTINATION, EXIT
from common.utils import get_message, send_message
from logs.configs.decorations import log
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError


# инициализация клиентоского логера
CLIENT_LOGGER = logging.getLogger('client')


@log
def create_presence(account_name):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    {
        'action': 'presence',
        'time': 1573760672.167031,
        'user': {'account_name': 'guest'}
    }
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(
        f'Сформировано {PRESENCE} сообщение пользоателя {account_name}')
    return out


@log
# +
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, my_username):
    """
    Функция - обработчик сообщений других пользователей, поступающих с сервера
    """
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and TEXT_MESSAGE in message and \
                    DESTINATION in message and \
                    message[DESTINATION] == my_username:
                print(f'Получено сообщение от пользователя '
                      f'{message[SENDER]}: {message[TEXT_MESSAGE]}')
                CLIENT_LOGGER.info(
                    f'Получено сообщение от пользователя '
                    f'{message[SENDER]}: {message[TEXT_MESSAGE]}')
            else:
                CLIENT_LOGGER.error(
                    f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            CLIENT_LOGGER.error('Не удалось декодировать полученное сообщение')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical('Потеряно соединение с сервером')
            break


@log
def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    CLIENT_LOGGER.debug(f'Cообщениe от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        TEXT_MESSAGE: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользоваетеля {to_user}')
    except:
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def user_interactive(sock, username):
    """
    Функция взаимодействия с пользователем, запрашивает команды,
    отправляет сообщения
    """
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершено соединение.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка необходимо, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробуйте снова',
                  '. help - вывесте поддерживаемые команды')


def print_help():
    """Функция выводящая справку по использованию"""
    print('Поддерживаемые команды:',
          'message - отправить сообщение. Кому и текст запросит отдельно',
          'help - вывести подсказки по командам',
          'exit - выход из программы.',
          sep='\n')


@log
def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        ADDRESS_ARGS, nargs='?',
        help=f'IP-адрес подключения, по умолчанию {DEFAULT_IP_ADDRESS}',
        default=DEFAULT_IP_ADDRESS
    )
    parser.add_argument(
        PORT_ARGS, nargs='?',
        help=f'Укажите порт подключения, по умолчанию {DEFAULT_PORT}',
        default=DEFAULT_PORT, type=int
    )
    parser.add_argument(
        '-n', '--name', nargs='?',
        choices=['listen', 'send'],
        help='Укажите режим рабоы, по умолчанию "listen"',
        default=None)

    args = parser.parse_args()

    if getattr(args, PORT_ARGS) < 1024 or getattr(args, PORT_ARGS) > 65535:
        CLIENT_LOGGER.critical(
            'Попытка запуска клиента с неподходящим номером порта:'
            f'{getattr(args, PORT_ARGS)}.\n'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.'
        )
        sys.exit(1)
    return {
        'address': getattr(args, ADDRESS_ARGS),
        'port': getattr(args, PORT_ARGS),
        'name': args.name
    }


def main():
    params = get_params()
    print('Консольный месседжер. Клиентский модуль.')

    CLIENT_LOGGER.critical(
        'Клиент запущен:\n'
        f'Адрес сервера: {params["address"]},'
        f'порт {params["port"]}, режим {params["name"]}'
    )

    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not params['name']:
        params['name'] = input('Введите имя пользователя: ')

    # устанавливаем соединене с сервером
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((params['address'], params['port']))

        # отправляем сообщение серверу о присутствии
        send_message(client_sock, create_presence(params['name']))
        server_connections_answer = process_ans(get_message(client_sock))
        CLIENT_LOGGER.info(
            f"Установлено соединение с сервером: {server_connections_answer}")
        print('Установлено соединение с сервером.')

    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        client_sock.close()
        sys.exit(1)

    except ServerError as error:
        CLIENT_LOGGER.error(f'''При установке соединения сервер
                            венул ошибку: {error.text}''')
        client_sock.close()
        sys.exit(1)

    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'''В ответе сервера отсутствует необходимое поле
                            {missing_error.missing_field}''')
        client_sock.close()
        sys.exit(1)

    except (ConnectionRefusedError, ConnectionError):
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {params["address"]}:'
            f'{params["port"]}, '
            'конечный компьютер отверг запрос на подключение.')

        client_sock.close()
        sys.exit(1)

    except Exception as ex:
        CLIENT_LOGGER.error(f'Что то еще пошло не так {ex}')

    else:
        # Если соединение с сервером установлено корректно,
        # запускаем клиентский процесс приеме сообщений
        receiver = threading.Thread(target=message_from_server,
                                    args=(client_sock, params['name']))
        receiver.daemon = True
        receiver.start()

        # запускаем отправку сообщений и взаимодействие с пользователем
        user_interface = threading.Thread(target=user_interactive,
                                          args=(client_sock, params['name']))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён,
        # то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках,
        # достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break

    finally:
        # на всяки случай закрываем сокет соединения с сервером
        client_sock.close()


if __name__ == '__main__':
    main()
