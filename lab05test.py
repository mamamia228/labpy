from lab05 import gen_bin_tree
import unittest


class TestGenBinTree(unittest.TestCase):

    def test_gen_bin_tree(self):
        # высота 0 -> дерево не создается
        self.assertIsNone(gen_bin_tree(0, 2))

        # отрицательная высота -> тоже None
        self.assertIsNone(gen_bin_tree(-1, 2))

        # высота строка -> берется 3, дерево создается
        tree = gen_bin_tree("ss", 2)
        self.assertEqual(tree["value"], 2)

        # некорректные функции -> используются стандартные
        tree = gen_bin_tree(2, 2, 12, 15)
        self.assertEqual(tree["left"]["value"], 3)
        self.assertEqual(tree["right"]["value"], 1)


if __name__ == "__main__":
    unittest.main()
