def get_task_index(tasks, argument):
    if argument == "":
        print("Вы не указали номер задачи")
        return None
    elif not argument.isdigit():
        print("Вы ввели не число")
        return None

    num = int(argument)-1

    if num < 0:
        print("Введите положительное число")
        return None
    elif num >= len(tasks):
        print("Задачи под таким номером нет в списке")
        return None

    return num
