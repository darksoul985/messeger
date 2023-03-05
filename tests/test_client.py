import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import PRESENCE, RESPONSE, ERROR, USER, ACCOUNT_NAME, \
    TIME, ACTION
from client import create_presence, process_ans


class ClientRunTastCase(unittest.TestCase):

    def test_create_prasence(self):
        '''создание сообщения'''
        example_data = {
            ACTION: PRESENCE,
            TIME: 1573760672.16031,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        testing_fanction = create_presence()
        testing_fanction[TIME] = 1573760672.16031
        self.assertDictEqual(testing_fanction, example_data)

    def test_process_ans(self):
        '''успешный ответ'''
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_process_ans_bed_request(self):
        '''сервер не доступен'''
        self.assertEqual(process_ans(
            {RESPONSE: 400, ERROR: 'Bad Request'}
        ), '400 : Bad Request')

    def test_process_ans_not_connect(self):
        '''неудачное подключение'''
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})
