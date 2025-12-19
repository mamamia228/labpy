import unittest
from lab02 import make_list, guess_number


class TestFunctions(unittest.TestCase):

    def test_make_list_basic(self):
        # проверяем обычный диапазон
        self.assertEqual(make_list(1, 3), [1, 2, 3])

    def test_make_list_negative(self):
        # проверяем, что отрицательные числа тоже работают
        self.assertEqual(make_list(-1, 1), [-1, 0, 1])

    def test_make_list_error(self):
        # проверяем ошибку, если начало больше конца
        with self.assertRaises(ValueError):
            make_list(5, 2)

    def test_guess_linear_found(self):
        # проверяем линейный поиск, когда число есть в списке
        value, tries = guess_number(3, [1, 2, 3, 4], "линейный")
        self.assertEqual(value, 3)
        self.assertEqual(tries, 3)

    def test_guess_binary_found(self):
        # проверяем бинарный поиск на неотсортированном списке
        value, tries = guess_number(4, [4, 1, 3, 2], "бинарный")
        self.assertEqual(value, 4)

    def test_guess_not_found(self):
        # проверяем, что если числа нет, выбрасывается ошибка
        with self.assertRaises(ValueError):
            guess_number(10, [1, 2, 3], "линейный")


if __name__ == "__main__":
    unittest.main()
