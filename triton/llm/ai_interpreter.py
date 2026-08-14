class AIInterpreter:
    def normalize(self, user_input: str) -> str:
        cleaned_input = user_input.lower().strip()

        normalized = self._normalize_tasks(cleaned_input, user_input)
        if normalized:
            return normalized

        normalized = self._normalize_notes(cleaned_input, user_input)
        if normalized:
            return normalized

        normalized = self._normalize_reminders(cleaned_input, user_input)
        if normalized:
            return normalized

        return user_input

    def _normalize_tasks(self, cleaned_input: str, original_input: str) -> str | None:
        if cleaned_input in [
            "what do i need to do",
            "what do i still need to do",
            "what should i work on"
        ]:
            return "show incomplete tasks"

        if cleaned_input in [
            "what are my tasks",
            "show me my tasks"
        ]:
            return "show tasks"

        return None

    def _normalize_notes(self, cleaned_input: str, original_input: str) -> str | None:
        if cleaned_input in [
            "what did i write down",
            "what are my notes",
            "show me my notes",
            "what notes do i have"
        ]:
            return "show notes"

        if cleaned_input.startswith("jot down "):
            note_text = original_input[9:].strip()
            return f"take note {note_text}"

        if cleaned_input.startswith("write down "):
            note_text = original_input[11:].strip()
            return f"take note {note_text}"

        return None

    def _normalize_reminders(self, cleaned_input: str, original_input: str) -> str | None:
        if cleaned_input in [
            "what reminders do i have",
            "show me my reminders",
            "list my reminders",
            "do i have reminders"
        ]:
            return "show reminders"

        return None