import unittest
from unittest.mock import Mock
from parameterized import parameterized
from main_lab10 import MathTools, check_even,NotificationService,UserManager,LibraryItem

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(MathTools(1,0).add_nums(),1)
    def test_minus(self):
        self.assertEqual(MathTools(1,0).minus(),1)
    def test_multiplication(self):
        self.assertEqual(MathTools(1,0).multiplication(),0)
    def test_div(self):
        self.assertEqual(MathTools(1, 1).division(), 1)
    def test_zero_div(self):
        with self.assertRaises(ZeroDivisionError):
            MathTools(1, 0).division()
class TestLibrary(unittest.TestCase):
    def test_details(self):
        original=LibraryItem('Clean Code', 'Robert Martin', 324).details()
        expected="Clean Code: Robert Martin (324)"
        self.assertEqual(original, expected)
class TestNotifyMock(unittest.TestCase):
    def test(self):
        mock_obj=Mock(spec=NotificationService)
        mock_obj.send.return_value=("Oleg", "qwerty123")
        result=UserManager("Oleg", mock_obj).notify_user("qwerty123")
        self.assertEqual(result, ("Oleg", "qwerty123"))
class TestEven(unittest.TestCase):
    @parameterized.expand([('even', 2, True), ('odd', 3, False),
                           ('even', 0, True),
                           ('even_minus', -2, True),
                           ('odd_minus', -5, False)])
    def test_even(self, name, num, expected):
        self.assertEqual(check_even(num), expected)

if __name__=='__main__':
    unittest.main()