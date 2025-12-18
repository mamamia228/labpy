# использование зависимостей
from ggg import two_sums
import unittest
# тесты
class TestTwoSums(unittest.TestCase):
    def test_simple(self):
        # стандартные
        self.assertEqual(two_sums([2, 7, 11, 15], 9), [0, 1], "ошибка в example 1")
        self.assertEqual(two_sums([3, 2, 4], 6), [1, 2], "ошибка в example 2")
        self.assertEqual(two_sums([3, 3], 6), [0, 1], "ошибка в example 3")
        # мои
        self.assertEqual(two_sums([1, 4, 5, 6, 1], 2), [0, 4], "ошибка при проверке значений в  частях массива")
        self.assertEqual(two_sums([1, 1, -1], -2), "решения нет", "ошибка при не нахождении решения")
        self.assertEqual(two_sums([1.1, 1.3, 3.1], 2.4), "один или несколько элементов не являются целыми числами",
                         "ошибка при использовании дробных знач")
# проверка тестов при запуске только при прямом вызове файла
if __name__ == "__main__":
    unittest.main()
