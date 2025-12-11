import requests
import json


def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    функция получает курсы валют с сервера ЦБ
    возвращает словарь вида {"USD": 93.2, ...}
    """

    # проверяем что передали список
    if not isinstance(currency_codes, list):
        raise TypeError("currency_codes должен быть списком")

    # пробуем сделать запрос
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.ConnectionError:
        raise ConnectionError("не могу подключиться к API")
    except requests.Timeout:
        raise ConnectionError("API долго не отвечает")
    except requests.HTTPError:
        raise ConnectionError("ошибка HTTP при запросе")

    # пробуем прочитать JSON
    try:
        data = r.json()
    except json.JSONDecodeError:
        raise ValueError("пришел плохой JSON")

    # проверяем, что есть раздел с валютами
    if "Valute" not in data:
        raise KeyError("нет раздела Valute в ответе")

    valutes = data["Valute"]
    result = {}

    # обрабатываем все нужные валюты
    for code in currency_codes:

        # проверяем
        # что валюта есть в данных
        if code not in valutes:
            raise KeyError(f"Нет валюты {code} в списке")

        info = valutes[code]
        value = info.get("Value")

        # проверяем, что курс то есть число
        if not isinstance(value, (int, float)):
            raise TypeError(f"некорректное значение курса для {code}")

        # записываем в результат
        result[code] = float(value)

    return result
