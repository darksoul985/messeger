# !usr/bin/env python
# -*- coding: utf-8 -*-
"""Программа-лаунчер"""

import subprocess
import time


PROCESSES = []


def start_app(app_name):
    return subprocess.Popen(
        f'bash -e python {app_name}', shell=True)


def main():
    global PROCESSES
    while True:
        ACTION = input('Выберите действие: q - выход,'
                       's - запустить сервер и клиенты,'
                       'x - закрыть все окна: ')
        if ACTION == 'q':
            break

        elif ACTION == 's':
            QUANTITY_CLIENTS = input('Введите количество клиентов: ')
            if QUANTITY_CLIENTS.isdigit():
                PROCESSES.append(start_app('server.py'))
                time.sleep(0.5)

                for _ in range(int(QUANTITY_CLIENTS)):

                    PROCESSES.append(start_app('client.py -n send'))
                    time.sleep(0.5)
            else:
                print('Должно быть числом')

        elif ACTION == 'x':
            for i in range(len(PROCESSES)):
                p = PROCESSES.pop()
                p.kill()
                print(p.pid, 'остановлен', sep=' ', end='\n')


if __name__ == '__main__':
    main()
