import sys; sys.path.append('..');
import unittest
from unittest.mock import patch

from iinput import iinput


class IinputTest(unittest.TestCase):


    def test_yn(self):
        test_data = {
            'y': 'y',
            'Y': 'y',
            ' Y ': 'y',
            'n': 'n',
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.yn(prompt='', default='d'), expected_return)

        with patch('builtins.input', side_effect=['', '  ', 'a', 'y']): 
            self.assertEqual(iinput.yn(prompt=''), 'y')
        
        with patch('builtins.input', side_effect=['', '  ', 'a', 'n']): 
            self.assertEqual(iinput.yn(prompt=''), 'n')


    def test_value(self):
        test_data = [
            ('abc', [str], 'abc'),
            (' abc ', [str], 'abc'),
            ('123', [str], '123'),
            ('123.4', [str], '123.4'),
            ('123', [int], 123),
            ('-123', [int], -123),
            ('123.4', [float], 123.4),
            ('-123.4', [float], -123.4),
            ('123.4', [int, float], 123.4),
            ('123', [int, float], 123),
            ('123abc', [int, float, str], '123abc'),
            ('True', [bool], True),
            ('1', [bool], True),
            ('False', [bool], False),
            ('0', [bool], False),
            ('1 2', [str], '1 2'),
            (' ', [str], 'd'),
            ('', [str], 'd'),
        ]
        for user_input, allowed_types, expected_return in test_data:
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.value(prompt='', allowed_types=allowed_types, default='d'), expected_return)

        for user_input, allowed_types, expected_return in test_data[:-2]:
            with patch('builtins.input', side_effect=['', '  ', user_input]): 
                self.assertEqual(iinput.value(prompt='', allowed_types=allowed_types, default=None), expected_return)


    def test_values(self):
        test_data = [
            ('abc 123 123.4 False True', [str], ['abc', '123', '123.4', 'False', 'True']),
            ('abc 123 123.4 False True', [str, int], ['abc', 123, '123.4', 'False', 'True']),
            ('abc 123 123.4 False True', [str, int, float], ['abc', 123, 123.4, 'False', 'True']),
            ('abc 123 123.4 False True', [str, int, float, bool], ['abc', 123, 123.4, False, True]),
            (' abc   123   123.4   False   True ', [str, int, float, bool], ['abc', 123, 123.4, False, True]),
            ('abc 123 123.4 False True', [int], [None, 123, None, None, None]),
            ('abc 123 123.4 False True', [float], [None, None, 123.4, None, None]),
            ('0 1', [int], [0, 1]),
            ('-1 +2', [int], [-1, 2]),
            ('0 1', [bool], [False, True]),
            ('0 1', [int, bool], [0, 1]),
            ('0 1 2', [bool], [False, True, None]),
            ('0 1 2', [int, bool], [0, 1, 2]),
            (' ', [str, int, float, bool], ['d']),
            (' ', [], ['d']),
        ]
        for user_input, allowed_types, expected_return in test_data:
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.values(prompt='', delimiter=' ', allowed_types=allowed_types, default=['d']), expected_return)


    def test_match_value(self):
        with patch('builtins.input', return_value='1'):
            self.assertTrue(iinput.match_value(prompt='', target=1))
        with patch('builtins.input', side_effect=['a', 'b', 'c']):
            self.assertTrue(iinput.match_value(prompt='', target='c'))
        with patch('builtins.input', side_effect=['a', 'b', 'c', 'd']):
            self.assertFalse(iinput.match_value(prompt='', target='d', max_attempts=3))


    def test_match_values(self):
        with patch('builtins.input', return_value=' 1, 2 , 3 '):
            self.assertTrue(iinput.match_values(prompt='', targets=[1,2,3]))

        with patch('builtins.input', side_effect=['', '', '1,2,3']):
            self.assertTrue(iinput.match_values(prompt='', targets=[1,2,3]))

        with patch('builtins.input', side_effect=['', '', '', '1,2,3']):
            self.assertFalse(iinput.match_values(prompt='', targets=[1,2,3], max_attempts=3))

    
    def test_boolean(self):
        test_data = {
            ' 1 ': True,
            '1': True,
            'true': True,
            'True': True,
            '0': False,
            'false': False,
            'False': False,
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.boolean(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['x', 'x', 'true']):
            self.assertTrue(iinput.boolean(prompt='', default='d'))


    def test_number(self):
        test_data = {
            ' 0 ': 0,
            '0': 0,
            '1': 1,
            '123': 123,
            '123.4': 123.4,
            '-123': -123,
            '+123.4': 123.4,
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.number(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['true', 'abc', 'abc123', '1 2', '', '123']):
            self.assertEqual(iinput.number(prompt=''), 123)


    def test_integer(self):
        test_data = {
            ' 0 ': 0,
            '0': 0,
            '1': 1,
            '-1': -1,
            ' -1 ': -1,
            '123': 123,
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.integer(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['true', 'abc', 'abc123', '1 2', '', '123.4', '123']):
            self.assertEqual(iinput.integer(prompt=''), 123)


    def test_floating_point(self):
        test_data = {
            ' 0.0 ': 0.0,
            '0.0': 0.0,
            '1.0': 1.0,
            '123.4': 123.4,
            '-123.4': -123.4,
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.floating_point(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['true', 'abc', 'abc123', '1 2', '', '123', '123.4']):
            self.assertEqual(iinput.floating_point(prompt=''), 123.4)


    def test_character(self):
        test_data = {
            'a': 'a',
            ' ': ' ',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.character(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['true', 'abc', 'abc123', '1 2', '', '123', '123.4', ' b ', 'a']):
            self.assertEqual(iinput.character(prompt=''), 'a')


    def test_string(self):
        test_data = {
            ' true ': 'true',
            'false': 'false',
            '0': '0',
            '1': '1',
            'abc': 'abc',
            'abc123': 'abc123',
            '123': '123',
            '123.4': '123.4',
            ' ': 'd',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.string(prompt='', default='d'), expected_return)


    def test_alpha(self):
        test_data = {
            ' true ': 'true',
            'false': 'false',
            'abc': 'abc',
            ' ': 'd',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.alpha(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['0', '1', 'abc123', '1 2', '', '123', '123.4', ' abc ']): 
            self.assertEqual(iinput.alpha(prompt=''), 'abc')


    def test_alphanumeric(self):
        test_data = {
            ' a1 ': 'a1',
            'abc123': 'abc123',
            ' true ': 'true',
            'false': 'false',
            '0': '0',
            '1': '1',
            ' ': 'd',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.alphanumeric(prompt='', default='d'), expected_return)

        with patch('builtins.input', side_effect=['123.4', '!', ' abc123 ']): 
            self.assertEqual(iinput.alphanumeric(prompt=''), 'abc123')
    

    def test_line(self):
        test_data = {
            ' abc123 ': ' abc123 ',
            ' ': ' ',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.line(prompt='', default='d'), expected_return)

        with patch('builtins.input', side_effect=['', '', ' hello, world! ']): 
            self.assertEqual(iinput.line(prompt='', default=None), ' hello, world! ')


    def test_lines(self):
        pass


    def test_selection(self):
        test_data = {
            ' a ': ('a', 1),
            'a': ('a', 1),
            'b': ('b', 2),
            'c': ('c', 3),
            '': ('d', None),
            '   ': ('d', None),
        }
        test_menu = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.selection(test_menu, default='d'), expected_return)

        with patch('builtins.input', side_effect=['', ' ', 'd', 'a']): 
            self.assertEqual(iinput.selection(test_menu), ('a', 1))


    def test_multiselection(self):
        test_data = {
            ' a ': {'a': 1},
            ' a, ': {'a': 1},
            'a': {'a': 1},
            'b': {'b': 2},
            'c': {'c': 3},
            'a,b': {'a': 1, 'b': 2},
            'a,b,c': {'a': 1, 'b': 2, 'c': 3},
            '': {'a': 1, 'd': None},
            '   ': {'a': 1, 'd': None},
        }
        test_menu = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.multiselection(test_menu, default=['a', 'd']), expected_return)

        with patch('builtins.input', side_effect=['', ' ', 'd', 'a,b,c,d', 'a,b,c']): 
            self.assertEqual(iinput.multiselection(test_menu), {'a': 1, 'b': 2, 'c': 3})


    def test_email(self):
        test_data = {
            ' test@test.com ': 'test@test.com',
            ' test@test.com 123': 'test@test.com',
            '': 'd',
            '   ': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.email(prompt='', default='d'), expected_return)
        
        with patch('builtins.input', side_effect=['', 'test', 'test@test.com']): 
            self.assertEqual(iinput.email(prompt='', default=None), 'test@test.com')


    def test_password(self):
        test_data = {
            ' abc123 ': ' abc123 ',
            ' ': ' ',
            '': 'd',
        }
        for user_input, expected_return in test_data.items():
            with patch('getpass.getpass', return_value=user_input):
                self.assertEqual(iinput.password(prompt='', default='d'), expected_return)

        with patch('getpass.getpass', side_effect=['', '', ' password ']): 
            self.assertEqual(iinput.password(prompt='', default=None), ' password ')


    def test_match_password(self):
        with patch('getpass.getpass', return_value='password123'):
            self.assertTrue(iinput.match_password(prompt='', target='password123'))
        with patch('getpass.getpass', side_effect=['a', 'b', 'password123']):
            self.assertTrue(iinput.match_password(prompt='', target='password123'))
        with patch('getpass.getpass', side_effect=['a', 'b', 'c', 'password123']):
            self.assertFalse(iinput.match_password(prompt='', target='password123', max_attempts=3))


    def test_regex(self):
        r = "[\w\.,]+@[\w\.,]+\.\w+"
        test_data = {
            ' test@test.com 123': 'test@test.com',
            'test@test.com': 'test@test.com',
        }
        for user_input, expected_return in test_data.items():
            with patch('builtins.input', return_value=user_input):
                self.assertEqual(iinput.regex(prompt='', r=r).group(0), expected_return)

        with patch('builtins.input', return_value=''):
            self.assertEqual(iinput.regex(prompt='', r=r, default='d'), 'd')

        with patch('builtins.input', side_effect=['', '  ', 'test', 'test@test.com']): 
            self.assertEqual(iinput.regex(prompt='', r=r).group(0), 'test@test.com')


    def test_wait_for_key_press(self):
        pass


    def test_wait_for_some_key_press(self):
        pass


    def test_wait_for_any_key_press(self):
        pass


if __name__ == '__main__':
    unittest.main()
