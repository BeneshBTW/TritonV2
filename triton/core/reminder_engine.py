from datetime import datetime


class ReminderEngine:
    def __init__(self, reminder_store):
        self.reminder_store = reminder_store

    def check_due_reminders(self) -> list[str]:
        reminders = self.reminder_store.load()
        due_messages = []

        now = datetime.now()
        changed = False

        for reminder in reminders:
            if reminder["completed"]:
                continue

            if reminder["delivered"]:
                continue

            if reminder["due"] is None:
                continue

            due_time = datetime.fromisoformat(reminder["due"])

            if due_time <= now:
                due_messages.append(reminder["text"])
                reminder["delivered"] = True
                changed = True

        if changed:
            self.reminder_store.save(reminders)

        return due_messages