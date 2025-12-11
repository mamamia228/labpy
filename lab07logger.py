import sys
import logging
from functools import wraps
import requests
import json
import math

def logger(func=None, *, handle=sys.stdout):
    """
    простой декоратор-логгер, handle может быть stdout, файлом или logging.Logger
    """

    # если декоратор вызвали как логгер
    if func is None:
        def deco(f):
            return logger(f, handle=handle)
        return deco

    @wraps(func)
    def wrapper(*args, **kwargs):
        # имя функции
        func_name = func.__name__
        # проверка это logger.Logger или обычный поток
        is_log_obj = isinstance(handle, logging.Logger)

        # сообщение о начале работы
        start_msg = f"START {func_name} args={args}, kwargs={kwargs}"
        if is_log_obj:
            handle.info(start_msg)        # если logging.Logger
        else:
            handle.write(start_msg + "\n")  # если stdout или файл

        try:
            result = func(*args, **kwargs)   # вызываем реальную функцию
        except Exception as e:
            # сообщение об ошибке
            err_msg = f"ERROR {func_name}: {type(e).__name__} - {e}"
            if is_log_obj:
                handle.error(err_msg)
            else:
                handle.write(err_msg + "\n")
            raise     # передаем ошибку дальше
        else:
            # сообщение об успешном завершении
            ok_msg = f"FINISH {func_name} -> {result!r}"
            if is_log_obj:
                handle.info(ok_msg)
            else:
                handle.write(ok_msg + "\n")
            return result

    return wrapper

logging.basicConfig(level=logging.INFO)

# логгер для записи в файл 
file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)
if not file_logger.handlers:           # чтобы не добавлять обработчик несколько раз
    fh = logging.FileHandler("currencies.log", encoding="utf-8")
    file_logger.addHandler(fh)

# логгер для квадратного уравнения 
quad_logger = logging.getLogger("QuadraticSolver")
quad_logger.setLevel(logging.INFO)
if not quad_logger.handlers:
    quad_logger.addHandler(logging.StreamHandler(sys.stdout))

@logger(handle=file_logger)   # все логирование делает декоратор
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    получение курсов валют
    """
    if not isinstance(currency_codes, list):
        raise TypeError("currency_codes должен быть списком")

    # пробуем отправить запрос
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except (requests.ConnectionError, requests.Timeout):
        raise ConnectionError(f"API недоступен: {url}")
    except requests.HTTPError:
        raise ConnectionError(f"ошибка HTTP при доступе к {url}")

    # пробуем распарсить JSON
    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise ValueError("некорректный JSON от API")

    if "Valute" not in data:
        raise KeyError("нет ключа 'Valute' в ответе")

    valute = data["Valute"]
    result = {}

    # перебираем нужные валюты
    for code in currency_codes:
        if code not in valute:
            raise KeyError(f"валюта '{code}' отсутствует в данных")

        rate = valute[code].get("Value")

        if not isinstance(rate, (int, float)):
            raise TypeError(f"неверный тип курса для '{code}'")

        result[code] = float(rate)

    return result

@logger(handle=quad_logger)  # логирование на консоль
def solve_quadratic(a, b, c):
    """
    Решение квадратного уравнения без логики логирования
    """
    # проверяем типы
    for x in (a, b, c):
        if not isinstance(x, (int, float)):
            raise TypeError("коэффициенты должны быть числами")

    # невалидное уравнение
    if a == 0 and b == 0:
        raise ValueError("a и b не могут быть оба 0")

    # линейный случай
    if a == 0:
        return [-c / b]

    # считаем дискриминант
    d = b * b - 4 * a * c

    if d < 0:
        quad_logger.warning(f"дискриминант < 0 (D={d}) корней нет")
        return []

    if d == 0:
        x = -b / (2 * a)
        return [x]

    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return [x1, x2]

if __name__ == "__main__":

    print("get_currencies (логирование в currencies.log)")

    try:
        get_currencies(['USD', 'EUR'])
        print("\nуспешный вызов get_currencies, проверьте файл currencies.log")
    except Exception:
        pass

    try:
        get_currencies(['USD', 'ZZZ'])
    except KeyError:
        print("\nвызов с KeyError, проверьте файл currencies.log (должен быть ERROR)")
    except Exception:
        pass

    try:
        get_currencies(['USD'], url="https://invalid-url-address.com/api")
    except ConnectionError:
        print("\nвызов с ConnectionError. проверьте файл currencies.log (должен быть ERROR)")
    except Exception:
        pass

    print("solve_quadratic (логирование в консоль через quad_logger)")

    print("\nтест 1: два корня (a=1, b=5, c=6)")
    solve_quadratic(1, 5, 6)

    print("\nтест 2: нет корней (a=1, b=0, c=1)")
    solve_quadratic(1, 0, 1)

    print("\nтест 3: TypeError (a='abc')")
    try:
        solve_quadratic("abc", 1, 1)
    except TypeError:
        print("TypeError")

    print("\nтест 4: ValueError (a=0, b=0)")
    try:
        solve_quadratic(0, 0, 5)
    except ValueError:
        print("ValueError")
