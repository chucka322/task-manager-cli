from pathlib import Path

from parser import parse_message
from storage import JsonTaskStorage
from task_manager import TaskManager


def main():
    base_dir = Path(__file__).resolve().parent
    storage = JsonTaskStorage(base_dir / "tasks.json")
    manager = TaskManager(storage)

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
