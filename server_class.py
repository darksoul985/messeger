import socket
import time
import logging
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, TIMEOUT_STEP
from common.argumentes import get_args_server
from common.utils import get_message, send_message
from logs.configs.decorations import log
from select import select

SERVER_LOGER = logging.getLogger('server')


class Server:
    def __init__(self, address, port):
        self.sock = None
        self.address = address
        self.port = port

        # словарь со списком клиентов
        self.clients = []

        # список сообщений на отправку
        self.messages = []

        # словарь содержащий сопоставленные имена и соответствующие им сокеты
        self.names = dict()

    def init_socket(self):
        SERVER_LOGER.info(f'Сервер запущен, порт для подключения: {self.port}, адрес с коорого прнимаются подключения: {self.address}. Если адрес не указан, принимаются соединения с любых адресов')
        with socket.create_server((self.address, self.port)) as server:
            # addr, prt = server.getsockname()
            SERVER_LOGER.info(
                f'Сервер запущен по адресу {self.address} Порт для подключения {self.port}')

            # слушаем порт и задаем тайм-аут сокета
            # server.settimeout(TIMEOUT_STEP)
            self.sock = server
            self.sock.listen(MAX_CONNECTIONS)
            print('Working...')
                
    def start(self):
        # инициализация сокета
        self.init_socket()
        # основной цикл программы сервера
        while True:
            # ждём подключения, если таймаут вышел, ловим исключение
            # try:
            socket_cl, address = self.sock.accept()
            SERVER_LOGER.info(f'Соединение установлено c {address}')

            # except KeyboardInterrupt:
            #     SERVER_LOGER.critical('Сервер принудительно остановлен')

            # except OSError:
            #     pass

            # else:
            #     SERVER_LOGER.info(f'Соединение установлено c {address}')

            timestr = time.ctime(time.time()) + '\n'
            socket_cl.send(timestr.enconde('ascii'))
            socket_cl.close()


            # read_cl, write_cl, err_lst = ([] for i in range(3))

            # # Проверяем на наличие ждущих клиентов
            # try:
            #     if self.clients:
            #         read_cl, write_cl, err_lst = select(self.clients, self.clients, [], 0)

            # except OSError:
            #     pass

            # # принимаем сообщение и если ошибка, исключаем клиента из списка клиентов
            # if read_cl:
            #     for client_with_message in read_cl:
            #         try:
            #             pass
            #         except:
            #             pass

        # def read_clients_messages(self, message, client):
        #     pass

if __name__ == '__main__':
    listen_address, listen_port = get_args_server()
    serv = Server(listen_address, listen_port)
    serv.start()
