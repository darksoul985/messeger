"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов. 
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом. 
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»). 
При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""

from subprocess import Popen, PIPE
from ipaddress import ip_address
from tabulate import tabulate


def host_ping(address, packeg=4, timeout=4):
    p = Popen(['ping', '-c', str(packeg), '-i', str(timeout), str(address)], shell=False, stdout=PIPE)
    p.wait()
    if p.returncode == 0:
        return True
    else:
        return False


def get_ip_address(address_list: list):
    result_ping = {"Узел доступен": [], "Узел не доступен": []}
    for address in address_list:
        try:
            address = ip_address(address)
        except:
            pass
        if host_ping(address):
            result_ping['Узел доступен'].append(address)
        else:
            result_ping['Узел не доступен'].append(address)
    return tabulate(result_ping, headers='keys', tablefmt='grid')


"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. 
Меняться должен только последний октет каждого адреса. 
По результатам проверки должно выводиться соответствующее сообщение.
"""
def host_range_ping(address: str):
    test_ip = address.split('.')
    start = int(input('Введите начало проверяемого отктета адреса: '))
    end = int(input("Введите сколько последовательных адресов проверить: "))
    if (start + end) <= 255:
        result_list = []
        for i in range(start, start+end):
            test_ip[-1] = str(i)
            result_list.append('.'.join(test_ip))
        return get_ip_address(result_list)
    else:
        print('Окончание заданного диапазона превышает максимально возможный адрес хоста 255.')
        return


def main():
    # addresses = ['ya.ru', '8.8.8.8', '192.168.0.1', '192.168.0.255']
    # print(get_ip_address(addresses))
    addresses = '8.8.8.0'
    print(host_range_ping(addresses))
    
if __name__ == '__main__':
    main()