# тесты для контроллеров currency и user

import unittest
from unittest.mock import Mock, ANY

from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController


class TestCurrencyController(unittest.TestCase):
    def setUp(self):
        # делаем mock базы, имитируем cursor.rowcount
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.controller = CurrencyController(self.mock_db)

    def test_create_currency(self):
        # имитируем, что база вернула id новой записи
        self.mock_db.execute.return_value = 5

        new_id = self.controller.create_currency("980", "UAH", "Украинская гривна", 2.30, 1)

        self.assertEqual(new_id, 5)
        # проверяем, что запрос был параметризованным (params переданы отдельно)
        self.mock_db.execute.assert_called_once_with(
            ANY,
            ("980", "UAH", "Украинская гривна", 2.30, 1),
            commit=True
        )

    def test_list_currencies(self):
        fake_rows = [{"id": 1, "char_code": "USD", "value": 90.0}]
        self.mock_db.execute.return_value = fake_rows

        rows = self.controller.list_currencies()

        self.assertEqual(rows[0]["char_code"], "USD")
        self.mock_db.execute.assert_called_once_with(ANY, fetch_all=True)

    def test_update_currency(self):
        # имитируем что обновили 1 строку
        self.mock_db.cursor.rowcount = 1

        self.controller.update_currency(
            2,
            char_code="EUR_NEW",
            value=77.0
        )

        # проверяем, что был UPDATE и был commit
        args, kwargs = self.mock_db.execute.call_args
        self.assertIn("UPDATE currency SET", args[0])
        self.assertTrue(kwargs.get("commit", False))

    def test_delete_currency(self):
        self.controller.delete_currency(1)
        self.mock_db.execute.assert_called_once_with(
            ANY,
            (1,),
            commit=True
        )


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_db.cursor = Mock()
        self.controller = UserController(self.mock_db)

    def test_create_user(self):
        self.mock_db.execute.return_value = 10

        new_id = self.controller.create_user("Петр Петрович")

        self.assertEqual(new_id, 10)
        self.mock_db.execute.assert_called_once_with(
            ANY,
            ("Петр Петрович",),
            commit=True
        )

    def test_list_users(self):
        fake_rows = [{"id": 1, "name": "Иван"}, {"id": 2, "name": "Сергей"}]
        self.mock_db.execute.return_value = fake_rows

        rows = self.controller.list_users()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["name"], "Сергей")
        self.mock_db.execute.assert_called_once_with(ANY, fetch_all=True)

    def test_update_user(self):
        self.controller.update_user(1, "Иван С.")
        self.mock_db.execute.assert_called_once_with(
            ANY,
            ("Иван С.", 1),
            commit=True
        )


if __name__ == "__main__":
    unittest.main()
