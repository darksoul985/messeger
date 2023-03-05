"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет
проверяться доступность сетевых узлов. Аргументом функции является список,
в котором каждый сетевой узел должен быть представлен именем хоста или
ip-адресом. В функции необходимо перебирать ip-адреса и проверять их
доступность с выводом соответствующего сообщения («Узел доступен»,
«Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address().
"""

from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(address, packeges=4, timeout='0.1'):

    checking = Popen(
        ['ping', '-c', str(packeges), '-i', timeout, str(address)],
        stdout=PIPE,
        encoding='utf-8')
    checking.wait()

    if checking.returncode == 0:
        return True
    else:
        return False


def checking_list(address_list):
    node_avaleble = []
    node_not_avaleble = []
    for address in address_list:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        if host_ping(address):
            node_avaleble.append(address)
        else:
            node_not_avaleble.append(address)

    return f'''Узел доступен: {', '.join(node_avaleble)}\r\nУзел не доступен: {', '.join([str(x) for x in node_not_avaleble])}'''


def main():
    addresses = ['yandex.ru', '2.2.2.2', '192.168.0.100', '192.168.0.101']
    print(checking_list(addresses))


if __name__ == "__main__":
    main()
