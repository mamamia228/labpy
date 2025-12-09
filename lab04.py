import timeit
import matplotlib.pyplot as plt
import random
from functools import *

def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
@lru_cache(None)
def fact_recursivee(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursivee(n - 1)

@lru_cache(None)
def fact_iterativee(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        # несколько повторов для усреднения
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)  # берём минимальное время из серии
    return total / len(data)


def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(60, 300, 30))

    res_recursive = []
    res_iterative = []
    res_rrecursive = []
    res_iiterative = []

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n], number=10000, repeat=5))
        res_iterative.append(benchmark(fact_iterative, [n], number=10000, repeat=5))
        res_rrecursive.append(benchmark(fact_recursivee, [n], number=10000, repeat=5))
        res_iiterative.append(benchmark(fact_iterativee, [n], number=10000, repeat=5))


    # Визуализация
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.plot(test_data, res_rrecursive, label="Рекурсивный c lru_cache")
    plt.plot(test_data, res_iiterative, label="Итеративный c lru_cache")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
