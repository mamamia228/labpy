from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader

from controllers.databasecontroller import DatabaseController
from controllers.pages import PagesController
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.usercurrencycontroller import UserCurrencyController
from utils.currencies_cbapi import get_currencies


def parse_post(body_bytes):
    text = body_bytes.decode("utf-8")
    qs = parse_qs(text)
    out = {}
    for k in qs:
        out[k] = qs[k][0]
    return out


class Handler(BaseHTTPRequestHandler):
    # "глобальные" ссылки меню
    def nav(self):
        return [
            {"href": "/", "caption": "Главная"},
            {"href": "/currencies", "caption": "Валюты"},
            {"href": "/users", "caption": "Пользователи"},
            {"href": "/author", "caption": "Об авторе"},
        ]

    def do_GET(self):
        u = urlparse(self.path)
        path = u.path
        qs = parse_qs(u.query)

        try:
            if path == "/":
                html = self.pages.render("index.html",
                                         title="Главная",
                                         myapp="Курсы валют",
                                         navigation=self.nav())
                return self._html(html)

            if path == "/author":
                html = self.pages.render("author.html",
                                         title="Об авторе",
                                         myapp="Курсы валют",
                                         navigation=self.nav())
                return self._html(html)

            if path == "/currencies":
                currencies = self.currency.list_currencies()

                # сообщения после обновления
                msg = qs.get("msg", [None])[0]
                ok = qs.get("ok", ["0"])[0] == "1"

                html = self.pages.render("currencies.html",
                                         title="Валюты",
                                         myapp="Курсы валют",
                                         navigation=self.nav(),
                                         currencies=currencies,
                                         update_message=msg,
                                         update_success=ok)
                return self._html(html)

            if path == "/currency/delete":
                cid = int(qs.get("id", ["0"])[0])
                if cid > 0:
                    self.currency.delete_currency(cid)
                return self._redir("/currencies")

            if path == "/update-currencies":
                # имитация "API" получаем новые значения и обновляем
                allc = self.currency.list_currencies()
                codes = [c["char_code"] for c in allc]
                rates = get_currencies(codes)
                self.currency.update_values_by_char(rates)
                return self._redir("/currencies?msg=Курсы+обновлены&ok=1")

            if path == "/users":
                users = self.user.list_users()
                html = self.pages.render("users.html",
                                         title="Пользователи",
                                         myapp="Курсы валют",
                                         navigation=self.nav(),
                                         users=users)
                return self._html(html)

            if path == "/user":
                uid = int(qs.get("id", ["0"])[0])
                user = self.user.get_user(uid)
                if not user:
                    return self._text(404, "Пользователь не найден")

                currencies = self.uc.currencies_for_user(uid)
                html = self.pages.render("user.html",
                                         title="Пользователь",
                                         myapp="Курсы валют",
                                         navigation=self.nav(),
                                         user=user,
                                         currencies=currencies)
                return self._html(html)

            if path == "/user/delete":
                uid = int(qs.get("id", ["0"])[0])
                if uid > 0:
                    self.user.delete_user(uid)
                return self._redir("/users")

            return self._text(404, "Нет такого маршрута")

        except Exception as e:
            return self._text(500, "Ошибка: " + str(e))

    def do_POST(self):
        try:
            ln = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(ln)
            form = parse_post(body)

            if self.path == "/currency/create":
                # без сложных проверок, просто переводим числа
                self.currency.create_currency(
                    form.get("num_code", ""),
                    form.get("char_code", ""),
                    form.get("name", ""),
                    float(form.get("value", "0")),
                    int(form.get("nominal", "1")),
                )
                return self._redir("/currencies")

            if self.path == "/currency/update":
                cid = int(form.get("id", "0"))
                self.currency.update_currency(
                    cid,
                    num_code=form.get("num_code", ""),
                    char_code=form.get("char_code", ""),
                    name=form.get("name", ""),
                    value=float(form.get("value", "0")),
                    nominal=int(form.get("nominal", "1")),
                )
                return self._redir("/currencies")

            if self.path == "/user/create":
                uid = self.user.create_user(form.get("name", ""))
                # для простоты подписываем на первую валюту если есть
                currs = self.currency.list_currencies()
                if currs:
                    self.uc.subscribe(uid, currs[0]["id"])
                return self._redir("/users")

            if self.path == "/user/update":
                uid = int(form.get("id", "0"))
                self.user.update_user(uid, form.get("name", ""))
                return self._redir("/users")

            return self._text(404, "Нет такого POST маршрута")

        except Exception as e:
            return self._text(500, "Ошибка: " + str(e))

    def _html(self, html_bytes):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_bytes)

    def _text(self, code, text):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    def _redir(self, to):
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()


def seed(db, cur_ctrl, user_ctrl, uc_ctrl):
    # стартовые данные чтобы не было пусто
    cur_ctrl.create_currency("840", "USD", "Доллар США", 90.0, 1)
    cur_ctrl.create_currency("978", "EUR", "Евро", 95.0, 1)
    cur_ctrl.create_currency("826", "GBP", "Фунт", 110.0, 1)

    u1 = user_ctrl.create_user("Иван")
    u2 = user_ctrl.create_user("Сергей")

    uc_ctrl.subscribe(u1, 1)
    uc_ctrl.subscribe(u1, 2)
    uc_ctrl.subscribe(u2, 2)


def main():
    db = DatabaseController()

    env = Environment(loader=FileSystemLoader("templates"))
    pages = PagesController(env)

    currency = CurrencyController(db)
    user = UserController(db)
    uc = UserCurrencyController(db)

    seed(db, currency, user, uc)

    def factory(*args, **kwargs):
        h = Handler(*args, **kwargs)
        h.pages = pages
        h.currency = currency
        h.user = user
        h.uc = uc
        return h

    srv = HTTPServer(("127.0.0.1", 8000), factory)
    print("Открывай: http://127.0.0.1:8000")
    srv.serve_forever()


if __name__ == "__main__":
    main()
