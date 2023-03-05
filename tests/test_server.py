import unittest
import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_PORT, MAX_CONNECTIONS, \
    SHORT_ADDRESS_ARGS, ADDRESS_ARGS, SHORT_PORT_ARGS, PORT_ARGS
from server import response_to_client_requeste, get_params, my_server_run


class ServerRunTestCase(unittest.TestCase):
    correct_response = {
        RESPONSE: 200
    }
    error_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_response_to_client_requeste_successfull(self):
        # корректный запрос
        example_messege = {
            ACTION: PRESENCE,
            TIME: 1114441414,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertDictEqual(
            response_to_client_requeste(example_messege),
            self.correct_response
        )

    def test_response_to_client_requeste_faild(self):
        # в цикле перебираем некорректные запросы

        # отсутствует признак времени
        example_messege_1 = {
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        # отсутствует ключ пользователя
        example_messege_2 = {
            ACTION: PRESENCE,
            TIME: 1114441414,
            }

        # пользователь не соответствует Guest
        example_messege_3 = {
            ACTION: PRESENCE,
            TIME: 1114441414,
            USER: {
                ACCOUNT_NAME: 'any'
            }
        }
        example_list = [
            example_messege_1,
            example_messege_2,
            example_messege_3
        ]

        # перебор в цикле не корректных запросов
        for pat in example_list:
            with self.subTest(pattern=pat):
                self.assertDictEqual(
                    response_to_client_requeste(pat),
                    self.error_response
                )


if __name__ == '__main__':
    unittest.main()
