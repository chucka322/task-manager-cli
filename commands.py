from storage import save_tasks
from validators import get_task_index


def add_task(tasks, argument):

    if argument == "":
        print("Вы не указали, какую задачу добавить")
    else:
        task = {
            "text": argument,
            "done": False
        }

        tasks.append(task)
        save_tasks(tasks)
        print(f'Задача "{argument}" добавлена!')


def show_one_task(index, task):
    text = task["text"]
    done = task["done"]

    if not done:
        pin = "[ ]"
    else:
        pin = "[x]"

    task_to_show = f'{index}. {pin} {text}'
    return task_to_show


def task_list(tasks, argument):
    if len(tasks) == 0:
        print("Список задач пуст")
        return

    if argument == "":
        all_tasks = []

        for index, task in enumerate(tasks, start=1):
            all_tasks.append(show_one_task(index, task))

        print(f'Список задач:\n{"\n".join(all_tasks)}')

    elif argument == "active":
        active_tasks = []

        for index, task in enumerate(tasks, start=1):

            done = task["done"]

            if not done:
                active_tasks.append(show_one_task(index, task))

        if len(active_tasks) == 0:
            print("Активных задач нет")
        else:
            print(f'Список активных задач:\n{"\n".join(active_tasks)}')

    elif argument == "done":
        done_tasks = []

        for index, task in enumerate(tasks, start=1):

            done = task["done"]

            if done:
                done_tasks.append(show_one_task(index, task))

        if len(done_tasks) == 0:
            print("Выполненных задач нет")
        else:
            print(f'Список выполненных задач:\n{"\n".join(done_tasks)}')

    else:
        print("Неизвестный фильтр")


def delete_task(tasks, argument):
    num = get_task_index(tasks, argument)

    if num is None:
        return

    task_to_delete = tasks.pop(num)
    save_tasks(tasks)
    print(f'Задача {task_to_delete["text"]} удалена')
    task_list(tasks, argument="")


def edit_task(tasks, argument):
    if argument == "":
        print("Укажите номер задачи и текст после команды, через пробел")
        return

    parts = argument.strip().split(maxsplit=1)

    if len(parts) < 2:
        print("Укажите номер задачи и текст после команды, через пробел")
        return

    index = get_task_index(tasks, parts[0])

    if index is None:
        return

    text_to_edit = parts[1]

    tasks[index]["text"] = text_to_edit
    save_tasks(tasks)
    print(f'Задача обновлена')
    task_list(tasks, argument="")


def done_task(tasks, argument):
    num = get_task_index(tasks, argument)

    if num is None:
        return

    if tasks[num]["done"]:
        print("Задача уже является выполненной")
    else:
        tasks[num]["done"] = True
        save_tasks(tasks)
        print(f'Задача {tasks[num]["text"]} выполнена!')
        task_list(tasks, argument="")


def undone_task(tasks, argument):
    num = get_task_index(tasks, argument)

    if num is None:
        return

    if not tasks[num]["done"]:
        print("Задача еще не выполнена")
    else:
        tasks[num]["done"] = False
        save_tasks(tasks)
        print(f'Задача {tasks[num]["text"]} не выполнена!')
        task_list(tasks, argument="")


def clear_tasks(tasks, argument=""):
    if len(tasks) < 1:
        print("Список уже пуст")
    else:
        tasks.clear()
        save_tasks(tasks)
        print("Все задачи из списка удалены")


def search(tasks, argument):
    if argument == "":
        print("Вы ввели пустую строку")
        return None

    search_list = []

    for index, item in enumerate(tasks, start=1):
        task_to_show = show_one_task(index, item)
        if argument in task_to_show:
            search_list.append(task_to_show)

    if len(search_list):
        print(f'Список задач со словом {argument}:\n{"\n".join(search_list)}')
    else:
        print("Такого слова нет в списке задач")


def stats(tasks, argument=""):
    total = len(tasks)
    done_count = sum(1 for task in tasks if task["done"])
    undone_count = total - done_count
    print(
        f'Всего задач: {total}\nВыполнено: {done_count}\nНе выполнено: {undone_count}')


def show_help(tasks, argument=""):
    print(
        "Список команд: /add_task, /delete_task, /edit_task, /done_task, /undone_task, /clear_tasks, /search, /stats, /task_list, /exit, /help")
