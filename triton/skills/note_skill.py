from triton.core.intent import Intent
from triton.core.response import Response
from triton.core.session import SessionContext
from triton.skills.base_skill import BaseSkill


class NoteSkill(BaseSkill):
    def __init__(self, session: SessionContext, user_memory_store):
        self.session = session
        self.user_memory_store = user_memory_store

    def can_handle(self, intent: Intent) -> bool:
        return intent.name in ["add_note", "show_notes", "remove_note", "clear_notes", "confirm_action", "cancel_action"]

    def execute(self, intent: Intent) -> Response:
        memory = self.user_memory_store.load()
        notes = memory.get("notes", [])

        if intent.name == "confirm_action":
            if self.session.pending_action != "clear_notes":
                return Response(
                    message="There is nothing to confirm right now.",
                    success=False
                ) 
            memory["notes"] = []
            self.user_memory_store.save(memory)
            self.session.pending_action = None
            self.session.pending_data = None

            return Response(
                message="All notes have been cleared.",
                success=True
            )
        
        if intent.name == "cancel_action":
            if self.session.pending_action != "clear_notes":
                return Response(
                    message="There is nothing to cancel right now.",
                    success=False
                ) 
            self.session.pending_action = None
            self.session.pending_data = None

            return Response(
                message="Action cancelled.",
                success=True
            )

        if intent.name == "add_note":
            notes.append(intent.text)

            memory["notes"] = notes
            self.user_memory_store.save(memory)

            return Response(
                message=f"Note saved: {intent.text}",
                success=True
            )
        
        if intent.name == "clear_notes":
            if len(notes) == 0:
                return Response(
                    message="you do not have any notes to clear.",
                    success=True
                )
            self.session.pending_action = "clear_notes"
            self.session.pending_data = {}

            return Response(
                message="Are you sure you want to clear all your notes? This action cannot be undone. Please say 'yes' to confirm or 'no' to cancel.",
                success=True
            )
        
        if intent.name == "remove_note":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the note numeber to remove, like: remove note 1",
                    success=False
            )

            note_index = int(intent.text) - 1

            if note_index < 0 or note_index >= len(notes):
                return Response(
                    message="That note number does not exist.",
                    success=False
                )
            
            removed_note = notes.pop(note_index)

            memory["notes"] = notes
            self.user_memory_store.save(memory)

            return Response(
                message=f"Removed note: {removed_note}",
                success=True
            )
        
        

        if len(notes) == 0:
            return Response(
                message="You do not have any notes yet.",
                success=True
            )

        notes_text = "\n".join(
            f"{index + 1}. {note}"
            for index, note in enumerate(notes)
        )

        return Response(
            message=f"Here are your notes:\n{notes_text}",
            success=True
        )