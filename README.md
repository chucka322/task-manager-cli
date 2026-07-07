# Task Manager CLI

A simple command-line task manager written in Python.

The app supports interactive mode and direct command-line usage. Tasks are stored locally in a JSON file.

## Features

- Add new tasks
- List all tasks
- Filter tasks by status
- Edit task text
- Delete tasks
- Mark tasks as todo, in progress, or done
- View detailed task information
- Search tasks by text
- Show task statistics
- Clear all tasks
- Store tasks locally in JSON

## Task statuses

Each task can have one of three statuses:

```text
todo
in-progress
done
```

## Requirements

- Python 3

## Running the app

Open the project folder in the terminal and run:

```bash
python main.py
```

On Windows, if `python` does not work, try:

```bash
py main.py
```

After launch, the app starts in interactive mode.

## Interactive commands

```text
help
add task text
list
list todo
list in-progress
list done
info
info task_number
edit task_number new text
delete task_number
mark-todo task_number
mark-in-progress task_number
mark-done task_number
search text
stats
clear
exit
```

## Direct CLI usage

You can also run commands directly from the terminal:

```bash
python main.py add "Buy groceries"
python main.py list
python main.py list done
python main.py mark-in-progress 1
python main.py mark-done 1
python main.py info 1
python main.py edit 1 "Buy groceries and cook dinner"
python main.py delete 1
python main.py stats
```

## Windows shortcut

On Windows, the project includes a `task-cli.bat` launcher.

It allows running commands from the project folder like this:

```bash
.\task-cli add "Buy groceries"
.\task-cli list
.\task-cli mark-in-progress 1
.\task-cli info 1
```

The `.bat` file starts `main.py` and passes all command arguments to it.

## Usage examples

Add a new task:

```bash
python main.py add "Buy groceries"
```

List all tasks:

```bash
python main.py list
```

List todo tasks:

```bash
python main.py list todo
```

List tasks in progress:

```bash
python main.py list in-progress
```

List done tasks:

```bash
python main.py list done
```

Mark a task as in progress:

```bash
python main.py mark-in-progress 1
```

Mark a task as done:

```bash
python main.py mark-done 1
```

Move a task back to todo:

```bash
python main.py mark-todo 1
```

Edit a task:

```bash
python main.py edit 1 "Buy groceries and cook dinner"
```

Show detailed task information:

```bash
python main.py info 1
```

Search tasks:

```bash
python main.py search groceries
```

Show task statistics:

```bash
python main.py stats
```

Delete a task:

```bash
python main.py delete 1
```

Delete all tasks:

```bash
python main.py clear
```

## Project structure

```text
main.py           app entry point
task.py           Task class
task_manager.py   TaskManager class and command handlers
storage.py        JSON storage logic
parser.py         command parser
task-cli.bat      Windows launcher
README.md         project documentation
.gitignore        ignored files
```

## Data storage

Tasks are stored locally in:

```text
tasks.json
```

The file is created automatically after adding tasks.

`tasks.json` contains local user data and is ignored by Git.

If the JSON file is corrupted, the app renames the broken file and starts with an empty task list.

## Project status

Completed.

## Project idea

This project is based on the Task Tracker project idea from roadmap.sh:

https://roadmap.sh/projects/task-tracker