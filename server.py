import argparse
import socket
import logging
# import time
import logs.configs.server_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    ERROR, DEFAULT_PORT, MAX_CONNECTIONS, SHORT_ADDRESS_ARGS, ADDRESS_ARGS, \
    SHORT_PORT_ARGS, PORT_ARGS, TIMEOUT_STEP, MESSAGE, TEXT_MESSAGE, \
    SENDER, RESPONSE_200, RESPONSE_400, DESTINATION, EXIT
from common.utils import get_message, send_message
from logs.configs.decorations import log
from select import select


SERVER_LOGER = logging.getLogger('server')


@log
def _get_presence_status(message: dict) -> bool:
    """
    обработчик запроса клиента, возвращает статус ответа
    """
    SERVER_LOGER.debug(f'Входящее сообщение клиента {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        return True
    else:
        return False


@log
def _check_presence_message(message: dict) -> bool:
    """
    обработчик запроса клиента с сообщением,
    возвращает булево значение
    """
    SERVER_LOGER.debug(f'Входящее сообщение от клиента {message}')
    if ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and DESTINATION in message and \
            SENDER in message and TEXT_MESSAGE in message:
        return True
    else:
        return False


@log
def _check_client_exit(message: dict) -> bool:
    if ACTION in message and message[ACTION] == EXIT and \
            ACCOUNT_NAME in message:
        return True
    else:
        return False


@log
def receive_messages(client, message, message_list, clients, names):
    """обрабатываем сообщения от клиента"""
    SERVER_LOGER.debug(f'Сообщение от клиента: {message}')
    # проверяем, является ли сообщением о присутствуии и отвечаем
    if _get_presence_status(message):
        # если пользователь ещё не зарегистрирован, регистрируем, иначе
        # отправляем ответ и завершаем соединение
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            return send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            clients.close()

    # если это сообщение, то добавляем в очередь сообщений.
    # ответ не требуется.
    elif _check_presence_message(message):
        message_list.append(message)
        return

    # если клиент выходит
    elif _check_client_exit:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return

    # иначе возаращаем неудачный запрос
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определенному клиенту.
    Принимает словарь сообщений, список зарегистрированных пользователей и
    слушающие сокеты. Ничего не возвращает.
    """
    if message[DESTINATION] in names and \
            names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGER.info(
            f'Отправлено сообщение пользователю {message[DESTINATION]}'
            f'от пользователя {message[DESTINATION]}.')
    elif message[DESTINATION] in names and \
            names[message[DESTINATION]] not in listen_socks:
        raise ValueError
    else:
        SERVER_LOGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на'
            f'сервере, отправка сообщения невозможна'
        )


@log
def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-' + SHORT_PORT_ARGS, '--' + PORT_ARGS,
        help=f'Укажите порт подключения, по умолчанию {DEFAULT_PORT}',
        default=DEFAULT_PORT, type=int
        )
    parser.add_argument(
        '-' + SHORT_ADDRESS_ARGS, '--' + ADDRESS_ARGS,
        help='Укажите IP-адрес подключения, по умолчанию все доступные',
        default=''
    )
    args = parser.parse_args()

    if getattr(args, PORT_ARGS) < 1024 or getattr(args, PORT_ARGS) > 65535:
        SERVER_LOGER.critical(
            f'Запуск сервера с порта не входящегов диапазон\n'
            f'{getattr(args, PORT_ARGS)} допустимые адреса от 1024 до 65535'
        )
        raise ValueError
    return {
        'address': getattr(args, ADDRESS_ARGS),
        'port': getattr(args, PORT_ARGS)
    }


def my_server_run():
    """Получаем параметны командной строки, если их нет,
    то загружаем параметры по умолчанию"""
    params = get_params()

    with socket.create_server((params['address'], params['port'])) as server:
        try:
            SERVER_LOGER.info(
                f'Сервер запущен по адресу {params["address"]}\n'
                f'Порт для подключения {params["port"]}')

            # слушаем порт и задаем тайм-аут сокета
            server.listen(MAX_CONNECTIONS)
            server.settimeout(TIMEOUT_STEP)

            # список клиентов, очередь сообщений
            all_clients = []
            messages = []

            # словарь, содержащий имена пользователей и соответствуещие им
            # сокеты
            names = dict()
            print('Working...')

            # основной цикл программы сервера
            while True:
                # ждём подключения, если таймаут вышел, ловим исключение
                try:
                    socket_cl, address = server.accept()
                    SERVER_LOGER.info(f'Соединение установлено c {address}')

                except OSError:
                    pass

                else:
                    SERVER_LOGER.info(f'Соединение установлено c {address}')
                    all_clients.append(socket_cl)

                read_cl = []
                write_cl = []
                err_lst = []
                # проверяем наличие ожидающих клиентов
                try:
                    read_cl, write_cl, err_lst = select(
                        all_clients, all_clients, [], 0)

                except OSError:
                    pass

                if read_cl:
                    for client in read_cl:
                        try:
                            receive_messages(
                                client, get_message(client), messages,
                                all_clients, names
                            )
                            SERVER_LOGER.info(
                                f'Получено сообщение {client}'
                            )
                        except Exception:
                            SERVER_LOGER.info(
                                f'Клиент {client.getpeername()} \
                                отключился от сервера.'
                            )
                            all_clients.remove(client)

                # если есть сообщения, обрабатываем каждое
                for mess in messages:
                    try:
                        process_message(mess, names, write_cl)
                    except Exception:
                        SERVER_LOGER.info(
                            f'Связь с клиентом {mess[DESTINATION]} потеряна'
                        )
                        all_clients.remove(names[mess[DESTINATION]])
                        del names[mess[DESTINATION]]
                messages.clear()

        except KeyboardInterrupt:
            SERVER_LOGER.critical('Сервер принудительно остановлен')

        except Exception as ex:
            SERVER_LOGER.error(f'Сервер отключен из-за ошибки {ex}')


def main():
    my_server_run()


if __name__ == '__main__':
    main()
