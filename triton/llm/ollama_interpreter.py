import requests

class OllamaInterpreter:
    def ask(self, prompt: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json = {
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data["response"].strip()
    
    def normalize(self, user_input: str) -> str:

        prompt = f"""
    You are Triton's command normalizer.

    convert the user's request into one of these commands:

    show tasks
    show incomplete tasks
    show notes
    show reminders
    take note <text>
    add task <text>
    add reminder <text>

    Rules:
    - Return only one command.
    - Use English only.
    - Do not translate.
    - Do not explain.
    - Do not add extra words.
    - Preserve the user's original task/note/reminder text as much as possible.

    User: {user_input}
    """

        command = self.ask(prompt).strip()
        print(f"Ollama returned: {command}")

        if self.is_valid_command(command):
            return command
        
        return user_input
    
    def is_valid_command(self, command: str) -> bool:
        allowed_exact = [
            "show tasks",
            "show incomplete tasks",
            "show notes",
            "show reminders",
        ]

        allowed_prefixes = [
            "take note ",
            "add task ",
            "add reminder ",
        ]

        if command in allowed_exact:
            return True
        
        for prefix in allowed_prefixes:
            if command.startswith(prefix):
                return True
            
        return False
    
