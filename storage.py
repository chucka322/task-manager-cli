import json
import os
from datetime import datetime


def save_broken_json():
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    tasks_broken = f"tasks_broken_{timestamp}.json"
    os.rename("tasks.json", tasks_broken)


def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            save_broken_json()
            return []

        for task in data:
            if not isinstance(task, dict):
                save_broken_json()
                return []

            if "text" not in task:
                save_broken_json()
                return []

            if "done" not in task:
                save_broken_json()
                return []

            if not isinstance(task["text"], str):
                save_broken_json()
                return []

            if not isinstance(task["done"], bool):
                save_broken_json()
                return []

        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Файл JSON поврежден")
        save_broken_json()
        return []


def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)
