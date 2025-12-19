# подписки пользователей на валюты.

class UserCurrencyController:
    def __init__(self, db):
        self.db = db

    def subscribe(self, user_id, currency_id):
        # без проверки на дубликаты, чтобы проще
        self.db.execute(
            "INSERT INTO user_currency VALUES(NULL, ?, ?)",
            (user_id, currency_id),
            commit=True
        )

    def currencies_for_user(self, user_id):
        # join чтобы показать валюты пользователя
        sql = """
        SELECT c.*
        FROM currency c
        JOIN user_currency uc ON uc.currency_id = c.id
        WHERE uc.user_id = ?
        ORDER BY c.id
        """
        return self.db.execute(sql, (user_id,), fetch_all=True)
