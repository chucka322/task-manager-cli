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

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self._save_broken_json()
                return []

            required_fields = [
                "text",
                "done",
                "task_id",
                "created_at",
                "updated_at",
            ]

            for task in data:
                if not isinstance(task, dict):
                    self._save_broken_json()
                    return []

                if not all(field in task for field in required_fields):
                    self._save_broken_json()
                    return []

                if not isinstance(task["text"], str):
                    self._save_broken_json()
                    return []

                if not isinstance(task["done"], bool):
                    self._save_broken_json()
                    return []

                if not isinstance(task["task_id"], str):
                    self._save_broken_json()
                    return []

                if not isinstance(task["created_at"], str):
                    self._save_broken_json()
                    return []

                if not isinstance(task["updated_at"], str):
                    self._save_broken_json()
                    return []

            task_list = []

            for task in data:
                task_list.append(
                    Task(
                        text=task["text"],
                        done=task["done"],
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
