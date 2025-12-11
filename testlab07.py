import unittest
import io

from lab07logger import get_currencies, logger

MAX_R_VALUE = 2000.0


class TestGetCurrencies(unittest.TestCase):
    """проверяем логику функции get_currencies"""

    def test_currency_usd_basic(self):
        """проверяем что USD возвращается и это число в разумных пределах"""
        codes = ['USD']
        data = get_currencies(codes)

        self.assertIn('USD', data)
        self.assertIsInstance(data['USD'], (int, float))
        self.assertGreaterEqual(data['USD'], 0)
        self.assertLessEqual(data['USD'], MAX_R_VALUE)

    def test_nonexistent_code_raises_keyerror(self):
        """несуществующий код валюты должен вызвать KeyError"""
        with self.assertRaises(KeyError):
            get_currencies(['XXX'])

    def test_bad_url_raises_connection_error(self):
        """плохой URL должен вызвать ConnectionError"""
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'], url="https://invalid-url-address.com")


class TestLoggerWithStream(unittest.TestCase):
    """проверяем работу декоратора logger с потоками"""

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped_ok(x):
            return x * 2

        @logger(handle=self.stream)
        def wrapped_fail():
            return get_currencies(['USD'], url="https://invalid-url-address.com")

        self.wrapped_ok = wrapped_ok
        self.wrapped_fail = wrapped_fail

    def tearDown(self):
        self.stream.close()

    def test_logger_success_info(self):
        """при успешном выполнении должны быть логи INFO и корректный результат"""
        result = self.wrapped_ok(5)
        logs = self.stream.getvalue()

        self.assertEqual(result, 10)
        self.assertIn("INFO: Started 'wrapped_ok'", logs)
        self.assertIn("INFO: Finished 'wrapped_ok'. Result: 10", logs)

    def test_logger_error_and_reraise(self):
        """при ошибке должны быть ERROR и исключение должно переходить дальше"""
        with self.assertRaises(ConnectionError):
            self.wrapped_fail()

        logs = self.stream.getvalue()

        self.assertIn("INFO: Started 'wrapped_fail'", logs)
        self.assertIn("ERROR: Failed 'wrapped_fail'", logs)
        self.assertNotIn("Finished 'wrapped_fail'", logs)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
