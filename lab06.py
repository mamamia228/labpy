import timeit
import matplotlib.pyplot as plt

# корневое значение по условию 
ROOT_GLOBAL = 13

# максимальная высота которую будем тестировать
H_MAX = 10

# создание одного узла дерева
def make_node(val):
    return {"val": val, "l": None, "r": None}

# рекурсивное построение структуры
def bad_rec_tree(h, r):
    # приводим параметры к int
    h = int(h)
    r = int(r)

    # если уровень 0 то узлов больше нет
    if h <= 0:
        return None

    # создаем основной узел для этого уровня
    n = make_node(r)

    # если высота = 1 то дальше структуры не строим
    if h == 1:
        return n

    # по условию вычисляем значения следующих элементов
    left_val = r + 1
    right_val = r - 1

    # Формируем подузлы следующего уровня
    n["l"] = bad_rec_tree(h - 1, left_val)
    n["r"] = bad_rec_tree(h - 1, right_val)

    return n


# итеративный вариант 
def bad_iter_tree(h, r):
    # приводим параметры к int
    try:
        h = int(h)
        r = int(r)
    except:
        return None

    # если высота < 1 то структура отсутствует
    if h < 1:
        return None

    # создаем корневой элемент
    root_node = make_node(r)

    # каждый элемент это узел и его уровень
    st = []
    st.append((root_node, 1))

    while len(st) > 0:
        node, level = st.pop()

        # На нужной высоте новые ветви больше не формируем
        if level >= h:
            continue

        # значение текущего узла
        v = node["val"]

        # значения подузлов 
        left_val = v + 1
        right_val = v - 1

        # создаем элементы следующего уровня
        left_node = make_node(left_val)
        right_node = make_node(right_val)

        # привязываем их к текущей структуре
        node["l"] = left_node
        node["r"] = right_node

        # добавляем в стек чтобы тоже обработать
        st.append((left_node, level + 1))
        st.append((right_node, level + 1))

    return root_node


# замер времени выполнения для одной высоты
def time_for_one(func, h):
    # Обертка для timeit
    def wrapper():
        func(h, ROOT_GLOBAL)

    # 300 повторов для усреднения
    t = timeit.timeit(wrapper, number=300)
    return t


def main():
    heights = []
    rec_times = []
    it_times = []

    # перебираем высоты от 1 до максимума
    x = 1
    while x <= H_MAX:
        heights.append(x)

        # время рекурсивного построения
        tr = time_for_one(bad_rec_tree, x)
        # время итеративного
        ti = time_for_one(bad_iter_tree, x)

        rec_times.append(tr)
        it_times.append(ti)

        # печатаем результаты по каждому уровню
        print("height =", x, "rec =", tr, "iter =", ti)

        x = x + 1

    plt.plot(heights, rec_times, "o-", label="рекурсивный")
    plt.plot(heights, it_times, "x-", label="итеративный")
    plt.xlabel("высота дерева")
    plt.ylabel("время")
    plt.title("сравнение рекурсивного и итеративного факториала")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
