import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from task import Task


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

    def _handle_broken_json(self):
        self._save_broken_json()
        return []

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self._save_broken_json()
                return []

            required_fields = [
                "text",
                "status",
                "task_id",
                "created_at",
                "updated_at",
            ]

            allowed_statuses = ["todo", "in-progress", "done"]

            for task in data:
                if not isinstance(task, dict):
                    return self._handle_broken_json()

                if not all(field in task for field in required_fields):
                    return self._handle_broken_json()

                if not all(isinstance(task[field], str) for field in required_fields):
                    return self._handle_broken_json()

                if task["status"] not in allowed_statuses:
                    return self._handle_broken_json()

            task_list = []

            for task in data:
                task_list.append(
                    Task(
                        text=task["text"],
                        status=task["status"],
                        task_id=task["task_id"],
                        created_at=task["created_at"],
                        updated_at=task["updated_at"],
                    )
                )

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
