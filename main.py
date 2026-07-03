from storage import load_tasks
from parser import parse_message
from commands import add_task, task_list, delete_task, edit_task, done_task, undone_task, clear_tasks, stats, show_help, search


def main():
    tasks = load_tasks()
    command_handlers = {}
    
    command_handlers = {
        "/add_task": add_task,
        "/task_list": task_list,
        "/delete_task": delete_task,
        "/edit_task": edit_task,
        "/done_task": done_task,
        "/clear_tasks": clear_tasks,
        "/undone_task": undone_task,
        "/stats": stats,
        "/help": show_help,
        "/search": search,
    }

    name = input("Привет! Введи свое имя: ")
    print(f'Привет, {name}! Введите /help для получения списка команд')

    while True:
        message = input("Введи команду: ").strip()

        if message == "":
            print("Вы ввели пустое сообщение")
            continue

        command, argument = parse_message(message)

        if command == "/exit":
            break
        elif command in command_handlers:
            command_handlers[command](tasks, argument)
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
