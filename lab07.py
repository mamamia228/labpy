import unittest
import io


from lab07logger import logger, get_currencies


class TestLoggerToStream(unittest.TestCase):
    """проверяем что декоратор пишет логи в поток"""

    def setUp(self):
        # поток в памяти вместо файла или консоли
        self.stream = io.StringIO()

        # оборачиваем функцию декоратором вручную
        @logger(handle=self.stream)
        def bad_request():
            # специально неверный адрес чтобы был ConnectionError
            return get_currencies(['USD'], url="https://invalid-url")

        self.bad_request = bad_request

    def test_error_logged_and_raised(self):
        # 1) должна подняться ошибка ConnectionError
        with self.assertRaises(ConnectionError):
            self.bad_request()

        # 2) в логах должно быть слово ERROR
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)

    def tearDown(self):
        # освобождаем ресурс 
        self.stream.close()
        del self.stream


if __name__ == "__main__":
    unittest.main(verbosity=2)
