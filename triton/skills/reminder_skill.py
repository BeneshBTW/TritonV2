from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill


class ReminderSkill(BaseSkill):
    def __init__(self, reminder_store):
        self.reminder_store = reminder_store

    def can_handle(self, intent: Intent) -> bool:
        return intent.name in [
            "add_reminder",
            "show_reminders",
            "remove_reminder",
            "complete_reminder"
        ]

    def execute(self, intent: Intent) -> Response:
        reminders = self.reminder_store.load()

        if intent.name == "add_reminder":
            reminder = {
                "text": intent.text,
                "due": None,
                "completed": False
            }

            reminders.append(reminder)
            self.reminder_store.save(reminders)

            return Response(
                message=f"Reminder added: {intent.text}",
                success=True
            )

        if intent.name == "show_reminders":
            if len(reminders) == 0:
                return Response(
                    message="You do not have any reminders yet.",
                    success=True
                )

            reminder_text = "\n".join(
                f"{index + 1}. {'[x]' if reminder['completed'] else '[ ]'} {reminder['text']}"
                for index, reminder in enumerate(reminders)
            )

            return Response(
                message=f"Here are your reminders:\n{reminder_text}",
                success=True
            )
        
        if intent.name == "complete_reminder":
            if not intent.text.isdigit():
                return Response(
                    message= "Please tell me the reminder number to complete, like: complete reminder 1",
                    success=False
                )
            reminder_index = int(intent.text) - 1

            if reminder_index < 0 or reminder_index >= len(reminders):
                return Response(
                    message="That reminder number does not exist"
                )     

            reminders[reminder_index]["completed"] = True
            self.reminder_store.save(reminders)

            return Response(
                message=f"Completed reminder: {reminders[reminder_index]['text']}",
                success=True
            )   

        if intent.name == "remove_reminder":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the reminder number to remove, like: remove reminder 1",
                    success=False
                )

            reminder_index = int(intent.text) - 1

            if reminder_index < 0 or reminder_index >= len(reminders):
                return Response(
                    message="That reminder number does not exist.",
                    success=False
                )

            removed_reminder = reminders.pop(reminder_index)
            self.reminder_store.save(reminders)

            return Response(
                message=f"Removed reminder: {removed_reminder['text']}",
                success=True
            )

        return Response(
            message="I do not know how to handle that reminder command.",
            success=False
        )