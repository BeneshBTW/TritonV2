class ReminderService:

    def __init__(self, reminder_store):
        self.reminder_store = reminder_store

    def get_reminders(self) -> list[dict]:
        return self.reminder_store.load()

    def add_reminder(self, text: str) -> dict:
        reminders = self.get_reminders()

        reminder = {
            "text": text,
            "due": None,
            "completed": False,
            "delivered": False
        }

        reminders.append(reminder)
        self.reminder_store.save(reminders)

        return reminder

    def remove_reminder(self, reminder_number: int) -> dict | None:
        reminders = self.get_reminders()
        reminder_index = reminder_number - 1

        if reminder_index < 0 or reminder_index >= len(reminders):
            return None

        removed_reminder = reminders.pop(reminder_index)
        self.reminder_store.save(reminders)

        return {
            "index": reminder_index,
            "reminder": removed_reminder
        }

    def restore_reminder(self, index: int, reminder: dict) -> None:
        reminders = self.get_reminders()
        reminders.insert(index, reminder)
        self.reminder_store.save(reminders)

    def complete_reminder(self, reminder_number: int) -> dict | None:
        reminders =self.get_reminders()
        reminder_index = reminder_number - 1

        if reminder_index < 0 or reminder_index >= len(reminders):
            return None
        
        reminders[reminder_index]["completed"] = True
        self.reminder_store.save(reminders)

        return reminders[reminder_index]
    
    def clear_reminders(self) -> list[dict]:
        reminders = self.get_reminders()
        self.reminder_store.save([])
        return  reminders
    
    def restore_all_reminders(self, reminders: list[dict]) -> None:
        self.reminder_store.save(reminders)

    def add_timed_reminder(self, text: str, due: str) -> dict:
        reminders = self.get_reminders()

        reminder = {
            "text": text,
            "due": due,
            "completed": False,
            "delivered": False
        }

        reminders.append(reminder)
        self.reminder_store.save(reminders)

        return reminder
        