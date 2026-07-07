import uuid
from datetime import datetime


class Task:
    def __init__(
        self, text, done=False, task_id=None, created_at=None, updated_at=None
    ):
        self.text = text
        self.done = done
        self.task_id = self.create_task_id() if task_id is None else task_id
        self.created_at = self.create_date() if created_at is None else created_at
        self.updated_at = self.create_date() if updated_at is None else updated_at

    def mark_done(self):
        self.done = True
        self.update_date()

    def mark_undone(self):
        self.done = False
        self.update_date()

    def edit_text(self, new_text):
        self.text = new_text
        self.update_date()

    def show_task(self):
        if self.done:
            pin = "[x]"
        else:
            pin = "[ ]"

        return f"{pin} {self.text}"

    def to_dict(self):
        return {
            "text": self.text,
            "done": self.done,
            "task_id": self.task_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def create_task_id(self):
        return str(uuid.uuid4())

    def create_date(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def update_date(self):
        self.updated_at = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
