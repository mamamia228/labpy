# имитация API просто возвращаем какие-то числа
# главная цель это показать, что обновление курсов работает

def get_currencies(codes):
    res = {}
    for code in codes:
        code = (code or "").upper()
        res[code] = round(70 + (len(code) * 1.7), 4)
    return res
