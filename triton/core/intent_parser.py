from triton.core.intent import Intent
from datetime import datetime, timedelta


class IntentParser:
    def parse(self, user_input: str) -> Intent:
        
        cleaned_input = user_input.lower().strip()

        if cleaned_input in ["undo", "undo last action", "restore last"]:
            return Intent(
                name="undo_action",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input in ["yes", "yeah", "yep", "sure", "y", "confirm"]:
            return Intent(
                name="confirm_action",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input in ["no", "nope", "nah", "n", "deny", "cancel"]:
            return Intent(
                name="cancel_action",
                text=user_input,
                confidence=1.0
            )

        if cleaned_input in ["hello", "hi", "hey"]:
            return Intent(
                name="greeting",
                text=user_input,
                confidence=1.0
            )

        if cleaned_input in ["what time is it", "time", "current time"]:
            return Intent(
                name="get_time",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input in ["what did i just say", "what was my last message", "repeat my last message"]:
             return Intent(
                name="session_recall",
                 text=user_input,
                 confidence=1.0
              )
        
        if cleaned_input.startswith("my name is "):
            name = user_input[11:].strip()
            return Intent(
                name="set_user_name",
                text=name,
                confidence=1.0
            )
        
        if cleaned_input in ["what is my name", "who am i", "whats my name"]:
            return Intent(
                name="get_user_name",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input.startswith("take note "):
            note_text = user_input[10:].strip()

            return Intent(
                name="add_note",
                text=note_text,
                confidence=1.0
            )
        
        if cleaned_input in ["show notes", "list notes", "what are my notes"]:
            return Intent(
                name="show_notes",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input.startswith("remove note "):
            note_number = cleaned_input.replace("remove note ", "").strip()

            return Intent(
                name="remove_note",
                text=note_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("delete note "):
            note_number = cleaned_input.replace("delete note ", "").strip()

            return Intent(
                name="remove_note",
                text=note_number,
                confidence=1.0
            )
        
        if cleaned_input in ["clear notes", "delete all notes", "remove all notes"]:
            return Intent(
                name="clear_notes",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input.startswith("add task "):
            task_text = user_input[9:].strip()

            return Intent(
                name="add_task",
                text=task_text,
                confidence=1.0
            )
        
        if cleaned_input in ["show tasks", "list tasks", "what are my tasks"]:
            return Intent(
                name="show_tasks",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input in ["show incomplete tasks", "show unfinished tasks"]:
            return Intent(
                name="show_incomplete_tasks",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input.startswith("complete task "):
            task_number = cleaned_input.replace("complete task ", "").strip()

            return Intent(
                name="complete_task",
                text=task_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("remove task "):
            task_number = cleaned_input.replace("remove task ", "").strip()

            return Intent(
                name="remove_task",
                text=task_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("delete task "):
            task_number = cleaned_input.replace("delete task ", "").strip()

            return Intent(
                name="remove_task",
                text=task_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("add reminder "):
            reminder_text = user_input[13:].strip()

            return Intent(
                name="add_reminder",
                text=reminder_text,
                confidence=1.0
            )
        
        if cleaned_input.startswith("remind me in ") and " to " in cleaned_input:
            after_in = cleaned_input.replace("remind me in ", "", 1)

            time_part, reminder_text = after_in.split(" to ", 1)

            words = time_part.split()

            if len(words) >= 2 and words[0].isdigit():
                amount = int(words[0])
                unit = words[1]

                if unit in ["minute", "minutes"]:
                    due_time = datetime.now() + timedelta(minutes=amount)

                    return Intent(
                        name="add_timed_reminder",
                        text=reminder_text,
                        confidence=1.0,
                        data={
                            "due": due_time.isoformat()
                        }
                    )
        
        if cleaned_input.startswith("remind me to ") and " to " in cleaned_input:
            reminder_text = user_input[13:].strip()

            return Intent(
                name="add_reminder",
                text=reminder_text,
                confidence=1.0
            )
        
        if cleaned_input in ["show reminders", "list reminders", "what are my reminders"]:
            return Intent(
                name="show_reminders",
                text=user_input,
                confidence=1.0
            )
        
        if cleaned_input.startswith("remove reminder "):
            reminder_number = cleaned_input.replace("remove reminder ", "").strip()

            return Intent(
                name="remove_reminder",
                text=reminder_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("delete reminder "):
            reminder_number = cleaned_input.replace("delete reminder ", "").strip()

            return Intent(
                name="remove_reminder",
                text=reminder_number,
                confidence=1.0
            )
        
        if cleaned_input.startswith("complete reminder "):
            reminder_number = cleaned_input.replace("complete reminder ", "").strip()

            return Intent(
                name="complete_reminder",
                text=reminder_number,
                confidence=1.0
            )
        
        if cleaned_input in ["clear reminders", "delete all reminders", "remove all reminders"]:
            return Intent(
                name="clear_reminders",
                text=user_input,
                confidence=1.0
            )
        

        return Intent(
            name="general_chat",
            text=user_input,
            confidence=0.0
        )