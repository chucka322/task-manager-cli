import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from parser import parse_message


class Task:
    def __init__(self, text, done=False):
        self.text = text
        self.done = done

    def mark_done(self):
        self.done = True

    def mark_undone(self):
        self.done = False

    def edit_text(self, new_text):
        self.text = new_text

    def show_task(self):
        if self.done:
            pin = "[x]"
        else:
            pin = "[ ]"

        return f"{pin} {self.text}"

    def to_dict(self):
        return {
            "text": self.text,
            "done": self.done
        }


class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.task_list = self.storage.load_tasks()
        self.command_handlers = self._build_command_handlers()

    def _build_command_handlers(self):
        command_handlers = {}

        for name in dir(self):
            if not name.startswith("cmd_"):
                continue

            method = getattr(self, name)

            if not callable(method):
                continue

            command = "/" + name[4:]
            command_handlers[command] = method

        return command_handlers

    def _save_tasks(self):
        self.storage.save_tasks(self.task_list)

    def _get_task_index(self, argument):
        if argument == "":
            print("Вы не указали номер задачи")
            return None

        if not argument.isdigit():
            print("Вы ввели не число")
            return None

        num = int(argument) - 1

        if num < 0:
            print("Введите положительное число")
            return None

        if num >= len(self.task_list):
            print("Задачи под таким номером нет в списке")
            return None

        return num

    def cmd_add_task(self, argument):
        if argument == "":
            print("Вы не указали, какую задачу добавить")
            return

        self.task_list.append(Task(argument))
        self._save_tasks()

        print(f'Задача "{argument}" добавлена!')

    def cmd_task_list(self, argument=""):
        if len(self.task_list) == 0:
            print("Список задач пуст")
            return

        if argument == "":
            all_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                task_to_show = f"{index}. {task.show_task()}"
                all_tasks.append(task_to_show)

            result = "\n".join(all_tasks)
            print(f"Список задач:\n{result}")

        elif argument == "done":
            done_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                if task.done:
                    task_to_show = f"{index}. {task.show_task()}"
                    done_tasks.append(task_to_show)

            if len(done_tasks) == 0:
                print("Выполненных задач нет")
            else:
                result = "\n".join(done_tasks)
                print(f"Список выполненных задач:\n{result}")

        elif argument == "active":
            active_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                if not task.done:
                    task_to_show = f"{index}. {task.show_task()}"
                    active_tasks.append(task_to_show)

            if len(active_tasks) == 0:
                print("Активных задач нет")
            else:
                result = "\n".join(active_tasks)
                print(f"Список активных задач:\n{result}")

        else:
            print("Неизвестный фильтр")

    def cmd_delete_task(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task_to_delete = self.task_list.pop(num)
        self._save_tasks()

        print(f'Задача "{task_to_delete.text}" удалена')
        self.cmd_task_list()

    def cmd_done_task(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task = self.task_list[num]

        if task.done:
            print("Задача уже является выполненной")
            return

        task.mark_done()
        self._save_tasks()

        print(f'Задача "{task.text}" выполнена!')
        self.cmd_task_list()

    def cmd_undone_task(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task = self.task_list[num]

        if not task.done:
            print("Задача уже активная")
            return

        task.mark_undone()
        self._save_tasks()

        print(f'Задача "{task.text}" снова активная!')
        self.cmd_task_list()

    def cmd_edit_task(self, argument):
        if argument == "":
            print("Укажите номер задачи и новый текст через пробел")
            return

        parts = argument.strip().split(maxsplit=1)

        if len(parts) < 2:
            print("Укажите номер задачи и новый текст через пробел")
            return

        index = self._get_task_index(parts[0])

        if index is None:
            return

        new_text = parts[1]

        self.task_list[index].edit_text(new_text)
        self._save_tasks()

        print("Задача обновлена")
        self.cmd_task_list()

    def cmd_search(self, argument):
        if argument == "":
            print("Вы ввели пустую строку")
            return

        search_list = []

        for index, task in enumerate(self.task_list, start=1):
            if argument.lower() in task.text.lower():
                task_to_show = f"{index}. {task.show_task()}"
                search_list.append(task_to_show)

        if len(search_list) == 0:
            print("Такого слова нет в списке задач")
        else:
            result = "\n".join(search_list)
            print(f'Список задач со словом "{argument}":\n{result}')

    def cmd_stats(self, argument=""):
        total = len(self.task_list)
        done_count = sum(1 for task in self.task_list if task.done)
        active_count = total - done_count

        print(
            f"Всего задач: {total}\n"
            f"Выполнено: {done_count}\n"
            f"Активных: {active_count}"
        )

    def cmd_clear_tasks(self, argument=""):
        if len(self.task_list) == 0:
            print("Список уже пуст")
            return

        self.task_list.clear()
        self._save_tasks()

        print("Все задачи удалены")

    def cmd_help(self, argument=""):
        commands = sorted(self.command_handlers.keys())
        commands.append("/exit")

        print("Список команд:")
        print(", ".join(commands))


class Storage(ABC):
    @abstractmethod
    def load_tasks(self):
        pass

    @abstractmethod
    def save_tasks(self, task_list):
        pass


class JsonTaskStorage(Storage):
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def _save_broken_json(self):
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        secure_file_name = os.path.basename(self.filename).replace(".", "_")
        broken_filename = f"tasks_broken_{secure_file_name}_{timestamp}.json"

        os.rename(self.filename, broken_filename)

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self._save_broken_json()
                return []

            for task in data:
                if not isinstance(task, dict):
                    self._save_broken_json()
                    return []

                if "text" not in task or "done" not in task:
                    self._save_broken_json()
                    return []

                if not isinstance(task["text"], str):
                    self._save_broken_json()
                    return []

                if not isinstance(task["done"], bool):
                    self._save_broken_json()
                    return []

            task_list = []

            for task in data:
                task_list.append(Task(task["text"], task["done"]))

            return task_list

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Файл JSON поврежден")
            self._save_broken_json()
            return []

    def save_tasks(self, task_list):
        dict_list = []

        for task in task_list:
            dict_list.append(task.to_dict())

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(dict_list, file, ensure_ascii=False, indent=4)


def main():
    storage = JsonTaskStorage("tasks.json")
    manager = TaskManager(storage)

    name = input("Привет! Введи свое имя: ")
    print(f'Привет, {name}! Введите /help для получения списка команд')

    while True:
        message = input("Введи команду: ").strip()

        if message == "":
            print("Вы ввели пустое сообщение")
            continue

        command, argument = parse_message(message)

        if command == "/exit":
            print("Пока!")
            break

        handler = manager.command_handlers.get(command)

        if handler is None:
            print("Неизвестная команда")
            continue

        handler(argument)


if __name__ == "__main__":
    main()
