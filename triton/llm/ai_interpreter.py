class AIInterpreter:
    def normalize(self, user_input: str) -> str:
        cleaned_input = user_input.lower().strip()

        if cleaned_input in [
            "what do i need to do",
            "what are my tasks",
            "what do i still need to do",
            "what should i work on",
            "show me my tasks"
        ]:
            return "show tasks"

        if cleaned_input in [
            "what did i write down",
            "what are my notes",
            "show me my notes",
            "what notes do i have"
        ]:
            return "show notes"

        if cleaned_input in [
            "what reminders do i have",
            "show me my reminders",
            "list my reminders"
        ]:
            return "show reminders"

        return user_input