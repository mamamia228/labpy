def gen_bin_tree(h=3, root_value=13,
                 left_op=lambda x: x + 1,
                 right_op=lambda x: x - 1):

    # пробуем перевести высоту в int
    try:
        h = int(h)
    except:
        print("не смог разобрать высоту беру 3")
        h = 3

    # пробуем перевести корень в int
    try:
        root_value = int(root_value)
    except:
        print("не смог разобрать корень беру 13")
        root_value = 13

    # проверяем чтобы высота была нормальной
    if h <= 0:
        print("высота должна быть > 0")
        return None

    # проверяем что передали функции
    if not callable(left_op):
        left_op = lambda x: x + 1
    if not callable(right_op):
        right_op = lambda x: x - 1

    # создаем корень дерева 
    root = {"value": root_value, "left": None, "right": None}

    # тут будут узлы текущего уровня
    current_level = [root]

    # начинаем с уровня 1 
    current_height = 1

    # пока не достигли нужной высоты
    while current_height < h:
        next_level = []   # сюда сложим узлы следующего уровня
        i = 0

        # перебираем узлы 
        while i < len(current_level):
            node = current_level[i]    # берем узел
            val = node["value"]        # значение в нем

            # создаем левого потомка
            try:
                left_val = left_op(val)
            except:
                left_val = None

            if left_val is not None:   # если функция не вернула None
                node["left"] = {"value": left_val, "left": None, "right": None}
                next_level.append(node["left"])

            # создаем правого потомка
            try:
                right_val = right_op(val)
            except:
                right_val = None

            if right_val is not None:
                node["right"] = {"value": right_val, "left": None, "right": None}
                next_level.append(node["right"])

            i += 1   # двигаемся дальше

        # переходим на новый уровень
        current_level = next_level
        current_height += 1

    return root


def print_tree(root):
    """вывод дерева"""
    if root is None:
        print("дерево пустое")
        return

    # стек для обхода
    stack = [(root, 0)]

    while stack:
        node, lvl = stack.pop()
        print("  " * lvl + str(node.get("value")))  # вывод значения с отступом

        # кладем правый, потом левый для того чтобы левый печатался ниже
        if node.get("right") is not None:
            stack.append((node["right"], lvl + 1))
        if node.get("left") is not None:
            stack.append((node["left"], lvl + 1))


def main():
    print("генерация бинарного дерева")

    # спрашиваем высоту
    h = input("введите высоту дерева: ")

    # спрашиваем корень
    r = input("введите значение корня: ")

    # если пусто берем значения по умолчанию
    if h.strip() == "":
        h_val = 3
    else:
        try:
            h_val = int(h)
        except:
            print("неверная высота беру 3")
            h_val = 3

    if r.strip() == "":
        r_val = 13
    else:
        try:
            r_val = int(r)
        except:
            print("неверный корень беру 13")
            r_val = 13

    # создаем дерево 
    tree = gen_bin_tree(h_val, r_val)

    print("\nполучившееся дерево:")
    print_tree(tree)


if __name__ == "__main__":
    main()
