class UserController:
    def __init__(self, db):
        self.db = db

    def list_users(self):
        return self.db.execute("SELECT * FROM user ORDER BY id", fetch_all=True)

    def create_user(self, name):
        
        if not name or not name.strip():
            name = "Без имени"
        return self.db.execute("INSERT INTO user VALUES(NULL, ?)", (name,), commit=True)

    def get_user(self, uid):
        return self.db.execute("SELECT * FROM user WHERE id = ?", (uid,), fetch_one=True)

    def update_user(self, uid, name):
        if not name or not name.strip():
            name = "Без имени"
        self.db.execute("UPDATE user SET name = ? WHERE id = ?", (name, uid), commit=True)

    def delete_user(self, uid):
        # сначала удаляем подписки, потом самого пользователя
        self.db.execute("DELETE FROM user_currency WHERE user_id = ?", (uid,), commit=False)
        self.db.execute("DELETE FROM user WHERE id = ?", (uid,), commit=True)
