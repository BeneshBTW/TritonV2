from triton.core.intent import Intent
from triton.core.response import Response
from triton.core.session import SessionContext
from triton.skills.base_skill import BaseSkill


class NoteSkill(BaseSkill):
    def __init__(self, session: SessionContext, note_service):
        self.session = session
        self.note_service = note_service

    def can_handle(self, intent: Intent) -> bool:
        if intent.name in ["confirm_action", "cancel_action"]:
            return self.session.pending_action == "clear_notes"
        
        if intent.name == "undo_action":
            return self.session.last_undo_action == "restore_note"
        
        return intent.name in ["add_note", "show_notes", "remove_note", "clear_notes"]

    def execute(self, intent: Intent) -> Response:
        notes = self.note_service.get_notes()

        if intent.name == "undo_action":
            if self.session.last_undo_action != "restore_note":
                return Response(
                    message="There is nothing to undo right now.",
                    success=False
                )
            
            note = self.session.last_undo_data["note"]
            index = self.session.last_undo_data["index"]

            self.note_service.restore_note(index, note)
            
            self.session.last_undo_action = None
            self.session.last_undo_data = None

            return Response(
                message=f"Restore note: {note}",
                success=True
            )

        if intent.name == "confirm_action":
            if self.session.pending_action != "clear_notes":
                return Response(
                    message="There is nothing to confirm right now.",
                    success=False
                ) 
            
            self.note_service.clear_notes()

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
            save_note = self.note_service.add_note(intent.text)

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
                    message="Please tell me the note numeber to remove. (ex. remove note)",
                    success=False
                )

            removed_data = self.note_service.remove_note(int(intent.text))

            if removed_data is None:
                return Response(
                    message= "That note number does not exist.",
                    success=False
                )
            
            self.session.last_undo_action = "restore_note"
            self.session.last_undo_data = removed_data

            return Response(
                message=f"Removed note: {removed_data['note']}",
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