from triton.core.intent import Intent


class IntentParser:
    def parse(self, user_input: str) -> Intent:
        
        cleaned_input = user_input.lower().strip()
        
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

        return Intent(
            name="general_chat",
            text=user_input,
            confidence=0.0
        )