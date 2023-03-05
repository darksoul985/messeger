"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""

from task_1 import checking_list

def host_range_ping(host_name: str):
    try:
        host_base = host_name.split('.')
    except:
        raise ValueError('Проверьте адрес хоста')
    start = input("Введите с какого адреса начинать проверку: ")
    end = input("Укажите, сколько адресов надо проверить: ")
    if (int(start) + int(end)) <= 255:
        host_list = []
        for i in range(int(start), int(start) + int(end)):
            host_base[-1] = str(i)
            print(host_base)
            host_list.append('.'.join(host_base))
        return checking_list(host_list)
    else:
        return print("Окончание проверяемого диапазона превышает 255")


def main():
    host = input('Введите адрес хоста')
    print(host_range_ping(host))


if __name__ == '__main__':
    main()
