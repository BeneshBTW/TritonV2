from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill
from triton.core.session import SessionContext
from triton.services.reminder_service import ReminderService


class ReminderSkill(BaseSkill):

    def __init__(self ,session , reminder_service):
        self.session = session
        self.reminder_service = reminder_service

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
            "cancel_action",
            "add_timed_reminder",
        ]

    def execute(self, intent: Intent) -> Response:
        reminders = self.reminder_service.get_reminders()

        if intent.name == "undo_action":
            if self.session.last_undo_action == "restore_reminder":
                reminder = self.session.last_undo_data["reminder"]
                index = self.session.last_undo_data["index"]

                self.reminder_service.restore_reminder(index, reminder)

                self.session.last_undo_action = None
                self.session.last_undo_data = None

                return Response(
                    message=f"Restore reminder: {reminder['text']}",
                    success=True
                )
        
            if self.session.last_undo_action == "restore_all_reminders":
                restored_reminders = self.session.last_undo_data["reminders"]

                self.reminder_service.restore_all_reminders(restored_reminders)

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
            
            self.reminder_service.clear_reminders()

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
            reminder = self.reminder_service.add_reminder(intent.text)

            return Response(
                message=f"Reminder added: {reminder['text']}",
                success=True
            )
        
        if intent.name == "add_timed_reminder":
            reminder = self.reminder_service.add_timed_reminder(
                intent.text,
                intent.data["due"]
            )

            return Response(
                message=f"Timed reminder added: {reminder['text']}",
                success= True
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
            
            completed_reminder = self.reminder_service.complete_reminder(int(intent.text))
            if completed_reminder is None:
                return Response(
                    message="That reminder number does not exist.",
                    success=False
                )
            
            return Response(
                message=f"Completed reminder: {completed_reminder['text']}",
                success=True
            )   

        if intent.name == "remove_reminder":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the reminder number to remove, like: remove reminder 1",
                    success= False
                )
            
            removed_data = self.reminder_service.remove_reminder(int(intent.text))

            if removed_data is None:
                return Response(
                    message="That reminder number does not exist.",
                    success=True
                )
            
            self.session.last_undo_action = "restore_reminder"
            self.session.last_undo_data = removed_data

            return Response(
                message=f"Removed reminder: {removed_data['reminder']['text']}",
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