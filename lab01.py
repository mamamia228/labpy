# тестовые входные данные
nums1 = [2, 7, 11, 15]
target1 = 9
nums2 = [3, 2, 4]
target2 = 6
nums3 = [3, 3]
target3 = 6
# в функции проходим в 2 цикла и сравниваем сумму элементов и таргет
def two_sums(nums, target):
    for a in range(len(nums)):
        # проверяем то что в массиве находится мин 2 элемента
        if len(nums) >= 2:
            # проверяем что элемент является целым числом
            if isinstance(nums[a], int):
                for aSled in range(a + 1, len(nums)):
                    if (nums[a] + nums[aSled]) == target:
                        return [a, aSled]
            else:
                return "один или несколько элементов не являются целыми числами"
        else:
            return "недостаточно элементов в массиве"

    return "решения нет"
print("example 1:", two_sums(nums1, target1))
print("example 2:", two_sums(nums2, target2))
print("example 3:", two_sums(nums3, target3))

