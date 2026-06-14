class NoteService:
    def __init__(self, user_memory_store):
        self.user_memory_store = user_memory_store

    def get_notes(self) -> list[str]:
        memory = self.user_memory_store.load()
        return memory.get("notes", [])

    def save_notes(self, notes: list[str]) -> None:
        memory = self.user_memory_store.load()
        memory["notes"] = notes
        self.user_memory_store.save(memory)

    def add_note(self, text: str) -> str:
        notes = self.get_notes()
        notes.append(text)
        self.save_notes(notes)
        return text

    def remove_note(self, note_number: int) -> dict | None:
        notes = self.get_notes()
        note_index = note_number - 1

        if note_index < 0 or note_index >= len(notes):
            return None

        removed_note = notes.pop(note_index)
        self.save_notes(notes)

        return {
            "index": note_index,
            "note": removed_note
        }

    def restore_note(self, index: int, note: str) -> None:
        notes = self.get_notes()
        notes.insert(index, note)
        self.save_notes(notes)

    def clear_notes(self) -> list[str]:
        notes = self.get_notes()
        self.save_notes([])
        return notes