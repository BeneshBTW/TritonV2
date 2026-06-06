from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill
from triton.core.session import SessionContext


class ReminderSkill(BaseSkill):
    def __init__(self ,session ,reminder_store):
        self.session = session
        self.reminder_store = reminder_store

    def can_handle(self, intent: Intent) -> bool:
        if intent.name in ["confirm_action", "cancel_action"]:
            return self.session.pending_action == "clear_reminders"
        
        if intent.name == "undo_action":
            return self.session.last_undo_action in ["restore_reminder", "restore_all_reminders"]

        return intent.name in [
            "add_reminder",
            "show_reminders",
            "remove_reminder",
            "complete_reminder",
            "clear_reminders",
            "confirm_action",
            "cancel_action"
        ]

    def execute(self, intent: Intent) -> Response:
        reminders = self.reminder_store.load()

        if intent.name == "undo_action":
            if self.session.last_undo_action == "restore_reminder":
                reminder = self.session.last_undo_data["reminder"]
                index = self.session.last_undo_data["index"]

                reminders.insert(index, reminder)
                self.reminder_store.save(reminders)

                self.session.last_undo_action = None
                self.session.last_undo_data = None

                return Response(
                    message=f"Restore reminder: {reminder['text']}",
                    success=True
                )
        
            if self.session.last_undo_action == "restore_all_reminders":
                restored_reminders = self.session.last_undo_data["reminders"]

                self.reminder_store.save(restored_reminders)

                self.session.last_undo_action = None
                self.session.last_undo_data = None

                return Response(
                    message="Restored all cleared reminders.",
                 success=True
                )
        
            return Response(
                message="There is nothing to undo right now.",
                success=True
            )
        
        if intent.name == "confirm_action":
            if self.session.pending_action != "clear_reminders":
                return Response(
                    message="There is nothing to confirm right now.",
                    success=False
                )
            
            self.session.last_undo_action = "restore_all_reminders"
            self.session.last_undo_data = {
                "reminders": reminders.copy()
            }
            
            self.reminder_store.save([])

            self.session.pending_action = None
            self.session.pending_data = None

            return Response(
                message="All reminder have been cleared.",
                success=True
            )
        
        if intent.name == "cancel_action":
            if self.session.pending_action is None:
                return Response(
                    message="There is nothing to canacel right now.",
                    success=False
                )
            
            self.session.pending_action = None
            self.session.pending_data = None
            return Response(
                message="Action cancled.",
                success=True
            )

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

            self.session.last_undo_action = "restore_reminder"
            self.session.last_undo_data = {
                "index" : reminder_index,
                "reminder" : removed_reminder
            }
            self.reminder_store.save(reminders)

            return Response(
                message=f"Removed reminder: {removed_reminder['text']}",
                success=True
            )
        
        if intent.name == "clear_reminders":
            if len(reminders) == 0:
                return Response(
                    message="You do not have any reminders to clear.",
                    success=True
                )
            
            self.session.pending_action = "clear_reminders"
            self.session.pending_data ={}

            return Response(
                message="Are you sure you want to clear all reminders? Type yes to confirm or no to cancel",
                success=True
            )

        return Response(
            message="I do not know how to handle that reminder command.",
            success=False
        )