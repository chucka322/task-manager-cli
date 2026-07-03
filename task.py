class Task:
    def __init__(self, text, done=False):
        self.text = text
        self.done = done

    def mark_done(self):
        self.done = True

    def mark_undone(self):
        self.done = False

    def edit_text(self, new_text):
        self.text = new_text

    def show_task(self):
        if self.done:
            pin = "[x]"
        else:
            pin = "[ ]"

        return f"{pin} {self.text}"

    def to_dict(self):
        return {
            "text": self.text,
            "done": self.done
        }