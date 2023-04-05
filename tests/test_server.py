import unittest
import os, sys
sys.path.append('../')
from common.variables import DEFAULT_PORT, ERROR, RESPONSE
from common.argumentes import get_args_server
from server import receive_messages, get_params, my_server_run


class ServerRunTestCase(unittest.TestCase):
    """
    Тут необходимо заменить проверяемую функцию, так как исходная принимает
    4 аргумента
    """
    correct_response = {
        RESPONSE: 200
    }
    error_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


    def test_get_args(self):
        correct_default_args = ('', DEFAULT_PORT)

        self.assertTupleEqual(correct_default_args, get_args_server())

#     def test_receive_messages_successfull(self):
#         # корректный запрос
#         example_messege = {
#             ACTION: PRESENCE,
#             TIME: 1114441414,
#             USER: {
#                 ACCOUNT_NAME: 'Guest'
#             }
#         }
#         self.assertDictEqual(
#             receive_messages(example_messege),
#             self.correct_response
#         )
# 
#     def test_receive_messages_faild(self):
#         # в цикле перебираем некорректные запросы
# 
#         # отсутствует признак времени
#         example_messege_1 = {
#             ACTION: PRESENCE,
#             USER: {
#                 ACCOUNT_NAME: 'Guest'
#             }
#         }
#         # отсутствует ключ пользователя
#         example_messege_2 = {
#             ACTION: PRESENCE,
#             TIME: 1114441414,
#             }
# 
#         # пользователь не соответствует Guest
#         example_messege_3 = {
#             ACTION: PRESENCE,
#             TIME: 1114441414,
#             USER: {
#                 ACCOUNT_NAME: 'any'
#             }
#         }
#         example_list = [
#             example_messege_1,
#             example_messege_2,
#             example_messege_3
#         ]
# 
#         # перебор в цикле не корректных запросов
#         for pat in example_list:
#             with self.subTest(pattern=pat):
#                 self.assertDictEqual(
#                     receive_messages(pat),
#                     self.error_response
#                 )


if __name__ == '__main__':
    unittest.main()
