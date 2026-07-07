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
        handler = manager.command_handlers.get(command)

        if handler is None:
            print("Unknown command")
            return

        handler(argument)
        return

    name = input("Hi! Enter your name: ")
    print(f"Hi, {name}! Type 'help' to see the list of commands")

    while True:
        message = input("Enter command: ").strip()

        if message == "":
            print("You entered an empty command")
            continue

        command, argument = parse_message(message)

        if command == "exit":
            print("Goodbye!")
            break

        handler = manager.command_handlers.get(command)

        if handler is None:
            print("Unknown command")
            continue

        handler(argument)


if __name__ == "__main__":
    main()
