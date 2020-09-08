def new_list():
    numbers = [-2, -1, 0, 1, 2, 3, 4, 5, 6]

    return [num for num in numbers if num > 0 and num % 2 == 0]


print(new_list())