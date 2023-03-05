import argparse
import socket
import logging
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    ERROR, DEFAULT_PORT, MAX_CONNECTIONS, SHORT_ADDRESS_ARGS, ADDRESS_ARGS, \
    SHORT_PORT_ARGS, PORT_ARGS, TIMEOUT_STEP, MESSAGE, TEXT_MESSAGE, \
    SENDER, RESPONSE_200, RESPONSE_400, DESTINATION, EXIT
from common.utils import get_message, send_message
from logs.configs.decorations import log
from select import select

SERVER_LOGER = logging.getLogger('server')

class Server:
    def run(self):
        # TODO сделать подгрузку настроек из файла DEFAULT_PORT, MAX_CONNECTIONS,TIMEOUT_STEP
        with socket.create_server(('', DEFAULT_PORT)) as server:
            try:
                SERVER_LOGER.info(
                    f'Сервер запущен по адресу {}\n'
                    f'Порт для подключения {}'))

                server.listen(MAX_CONNECTIONS)
                server.settimeout(TIMEOUT_STEP)
                print('Working...')
                # список клиентов, очередь сообщений
                all_clients = []
                messages = []

                names = dict()

                while True:
                    try:
                        clients, address = server.accept()
                        SERVER_LOGER.info(f'Соединение установлено c {address}')
                    except OSError:
                        pass
                    else:
                        all_clients.append(clients)

                    ready_clients = []
                    write_clients = []
                    err_list = []
                    # проверяем наличие ожидающих клиенов
                    try:
                        ready_clients, write_clients, err_list = select(all_clients, )