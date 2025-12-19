# controllers/currencycontroller.py

class CurrencyController:
    def __init__(self, db):
        self.db = db

    def list_currencies(self):
        return self.db.execute("SELECT * FROM currency ORDER BY id", fetch_all=True)

    def create_currency(self, num_code, char_code, name, value, nominal):
        sql = "INSERT INTO currency VALUES(NULL, ?, ?, ?, ?, ?)"
        return self.db.execute(sql, (num_code, char_code, name, value, nominal), commit=True)

    def update_currency(self, cid, **fields):
        # делаю просто обновляю то что пришло из формы
        # поля идут как kwargs
        parts = []
        vals = []
        for k in fields:
            parts.append(k + " = ?")
            vals.append(fields[k])

        vals.append(cid)
        sql = "UPDATE currency SET " + ", ".join(parts) + " WHERE id = ?"
        self.db.execute(sql, vals, commit=True)

    def delete_currency(self, cid):
        self.db.execute("DELETE FROM currency WHERE id = ?", (cid,), commit=True)

    def update_values_by_char(self, rates):
        # rates = {'USD': 91.0, 'EUR': 99.0}
        for code in rates:
            self.db.execute(
                "UPDATE currency SET value = ? WHERE char_code = ?",
                (rates[code], code),
                commit=False
            )
        self.db.conn.commit()
