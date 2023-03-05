import sys
import os
import logging
import argparse
import traceback
import inspect
sys.path.append(os.path.join(os.getcwd(), '../..'))
import logs.configs.client_log_config
import logs.configs.server_log_config

if argparse.ArgumentParser().prog == 'server.py':
    LOGGER = logging.getLogger('server')
if argparse.ArgumentParser().prog == 'client.py':
    LOGGER = logging.getLogger('client')


def log(func):
    """декоратор"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        LOGGER.debug(f'Вызвана функция {func} с параметрами {args}, {kwargs}.\n'
                     f'Вызов из модуля {func.__module__}\n'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.\n'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return result
    return wrapper
