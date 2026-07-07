import sys

from pathlib import Path
from parser import parse_message
from storage import JsonTaskStorage
from task_manager import TaskManager


def main():
    base_dir = Path(__file__).resolve().parent
    storage = JsonTaskStorage(base_dir / "tasks.json")
    manager = TaskManager(storage)
    if len(sys.argv) > 1:
        command = sys.argv[1]
        argument = " ".join(sys.argv[2:])

        cli_commands = {
            "add": "/add_task",
            "list": "/task_list",
            "delete": "/delete_task",
            "update": "/edit_task",
            "mark-done": "/mark_done",
            "mark-in-progress": "/mark_in_progress",
            "mark-todo": "/mark_todo",
            "info": "/task_info",
            "stats": "/stats",
            "clear": "/clear_tasks",
            "help": "/help",
        }

        translated_command = cli_commands.get(command)
        handler = manager.command_handlers.get(translated_command)

        if handler is None:
            print("Неизвестная команда")
            return

        handler(argument)
        return

    name = input("Привет! Введи свое имя: ")
    print(f"Привет, {name}! Введите /help для получения списка команд")

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
