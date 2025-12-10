import pprint   # модуль для отображения словарей

# функция спрашивает у пользователя height и root и возвращает два числа или None, None если была ошибка
def get_user_data():
    print("генерация бинарного дерева")
    print("если ничего не вводить будут значения по умолчанию: height = 3, root = 13")

    height = input("введите высоту дерева: ")
    root = input("введите корень дерева: ")

    # если пользователь ничего не написал то ставим значения по умолчанию
    if height == "":
        height = 3
    else:
        # проверяем что введено число
        if height.isdigit():
            height = int(height)
        else:
            print("ошибка: height должно быть целым числом")
            return None, None

    if root == "":
        root = 13
    else:
        if root.isdigit():
            root = int(root)
        else:
            print("ошибка: root должно быть целым числом")
            return None, None

    return height, root   # возвращаем два значения



# Функция генерирует бинарное дерево по правилу, что левый потомок = root + 1, правый потомок = root - 1, height —это то сколько уровней еще надо строить
def gen_bin_tree(height, root):

    # если высота 1, то это лист (без потомков)
    if height <= 1:
        return {root: []}

    # вычисляем значения потомков 
    left_value = root + 1
    right_value = root - 1

    # рекурсивно делаем левое и правое поддерево с высотой -1
    left_tree = gen_bin_tree(height - 1, left_value)
    right_tree = gen_bin_tree(height - 1, right_value)

    # возвращаем дерево
    return {root: [left_tree, right_tree]}

h, r = get_user_data()

# если ошибок не было, строим дерево
if h is not None and r is not None:
    tree = gen_bin_tree(h, r)
    print("полученное дерево:")
    pprint.pprint(tree)   
