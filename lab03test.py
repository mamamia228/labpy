import unittest
from lab03 import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_one(self):
        # высота 1 -> лист без потомков
        self.assertEqual(gen_bin_tree(1, 5), {5: []})

    def test_height_two(self):
        # высота 2 -> два потомка
        self.assertEqual(
            gen_bin_tree(2, 1),
            {1: [{2: []}, {0: []}]}
        )

    def test_height_three(self):
        # проверка дерева с высотой 3
        tree = gen_bin_tree(3, 0)
        self.assertIn(0, tree)

    def test_negative_height(self):
        # отрицательная высота -> тоже лист
        self.assertEqual(gen_bin_tree(-1, 10), {10: []})


if __name__ == "__main__":
    unittest.main()
