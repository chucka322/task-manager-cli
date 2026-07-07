from task import Task


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

            command = name[4:].replace("_", "-")
            command_handlers[command] = method

        return command_handlers

    def _save_tasks(self):
        self.storage.save_tasks(self.task_list)

    def _get_task_index(self, argument):
        if argument == "":
            print("Task number was not provided")
            return None

        if not argument.isdigit():
            print("Task number must be a number")
            return None

        num = int(argument) - 1

        if num < 0:
            print("Enter a positive number")
            return None

        if num >= len(self.task_list):
            print("There is no task with this number")
            return None

        return num

    def cmd_add(self, argument):
        if argument == "":
            print("Task text was not provided")
            return

        self.task_list.append(Task(argument))
        self._save_tasks()

        print(f'Task "{argument}" added successfully')

    def cmd_list(self, argument=""):
        if len(self.task_list) == 0:
            print("Task list is empty")
            return

        if argument == "":
            all_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                task_to_show = f"{index}. {task.show_task()}"
                all_tasks.append(task_to_show)

            result = "\n".join(all_tasks)
            print(f"\nTask list:\n\n{result}\n")

        elif argument == "done":
            done_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                if task.status == "done":
                    task_to_show = f"{index}. {task.show_task()}"
                    done_tasks.append(task_to_show)

            if len(done_tasks) == 0:
                print("There are no done tasks")
            else:
                result = "\n".join(done_tasks)
                print(f"\nDone tasks:\n\n{result}\n")

        elif argument == "in-progress":
            in_progress_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                if task.status == "in-progress":
                    task_to_show = f"{index}. {task.show_task()}"
                    in_progress_tasks.append(task_to_show)

            if len(in_progress_tasks) == 0:
                print("There are no tasks in progress")
            else:
                result = "\n".join(in_progress_tasks)
                print(f"\nTasks in progress:\n\n{result}\n")

        elif argument == "todo":
            todo_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                if task.status == "todo":
                    task_to_show = f"{index}. {task.show_task()}"
                    todo_tasks.append(task_to_show)

            if len(todo_tasks) == 0:
                print("There are no todo tasks")
            else:
                result = "\n".join(todo_tasks)
                print(f"\nTodo tasks:\n\n{result}\n")

        else:
            print(
                "Unknown filter. Use: todo, in-progress, done, "
                "or leave the argument empty to show all tasks"
            )

    def cmd_delete(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task_to_delete = self.task_list.pop(num)
        self._save_tasks()

        print(f'Task "{task_to_delete.text}" deleted')
        self.cmd_list()

    def cmd_mark_done(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task = self.task_list[num]

        if task.status == "done":
            print("Task is already done")
            return

        task.mark_done()
        self._save_tasks()

        print(f'Task "{task.text}" marked as done')
        self.cmd_list()

    def cmd_mark_in_progress(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task = self.task_list[num]

        if task.status == "in-progress":
            print("Task is already in progress")
            return

        task.mark_in_progress()
        self._save_tasks()

        print(f'Task "{task.text}" marked as in progress')
        self.cmd_list()

    def cmd_mark_todo(self, argument):
        num = self._get_task_index(argument)

        if num is None:
            return

        task = self.task_list[num]

        if task.status == "todo":
            print("Task is already todo")
            return

        task.mark_todo()
        self._save_tasks()

        print(f'Task "{task.text}" marked as todo')
        self.cmd_list()

    def cmd_edit(self, argument):
        if argument == "":
            print("Provide task number and new text separated by a space")
            return

        parts = argument.strip().split(maxsplit=1)

        if len(parts) < 2:
            print("Provide task number and new text separated by a space")
            return

        index = self._get_task_index(parts[0])

        if index is None:
            return

        new_text = parts[1]

        self.task_list[index].edit_text(new_text)
        self._save_tasks()

        print("Task updated")
        self.cmd_list()

    def cmd_search(self, argument):
        if argument == "":
            print("Search query is empty")
            return

        search_list = []

        for index, task in enumerate(self.task_list, start=1):
            if argument.lower() in task.text.lower():
                task_to_show = f"{index}. {task.show_task()}"
                search_list.append(task_to_show)

        if len(search_list) == 0:
            print("No tasks found")
        else:
            result = "\n".join(search_list)
            print(f'Tasks matching "{argument}":\n{result}')

    def cmd_stats(self, argument=""):
        total = len(self.task_list)
        done_count = sum(1 for task in self.task_list if task.status == "done")
        todo_count = sum(1 for task in self.task_list if task.status == "todo")
        in_progress_count = total - done_count - todo_count

        print(
            f"Total tasks: {total}\n"
            f"Done: {done_count}\n"
            f"In progress: {in_progress_count}\n"
            f"Todo: {todo_count}"
        )

    def cmd_clear(self, argument=""):
        if len(self.task_list) == 0:
            print("Task list is already empty")
            return

        self.task_list.clear()
        self._save_tasks()

        print("All tasks deleted")

    def cmd_help(self, argument=""):
        commands = sorted(self.command_handlers.keys())
        commands.append("exit")

        print("Available commands:")
        print(", ".join(commands))

    def cmd_info(self, argument=""):
        if len(self.task_list) == 0:
            print("Task list is empty")
            return

        if argument == "":
            all_tasks = []

            for index, task in enumerate(self.task_list, start=1):
                task_data = task.to_dict()
                task_to_show = (
                    f"{index}\n"
                    f"Task: {task_data['text']}\n"
                    f"Status: {task_data['status']}\n"
                    f"Task ID: {task_data['task_id']}\n"
                    f"Created at: {task_data['created_at']}\n"
                    f"Updated at: {task_data['updated_at']}\n"
                )
                all_tasks.append(task_to_show)

            result = "\n".join(all_tasks)
            print(f"\nTask list:\n\n{result}")

        elif argument.isdigit():
            index = self._get_task_index(argument)

            if index is None:
                return

            task = self.task_list[index]
            task_data = task.to_dict()
            task_to_show = (
                f"{argument}\n"
                f"Task: {task_data['text']}\n"
                f"Status: {task_data['status']}\n"
                f"Task ID: {task_data['task_id']}\n"
                f"Created at: {task_data['created_at']}\n"
                f"Updated at: {task_data['updated_at']}\n"
            )
            print(task_to_show)

        else:
            print("Unknown argument")
