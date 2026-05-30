import json 
from pathlib import Path

class UserMemoryStore:
    def __init__(self, file_path = "triton/data/user_memory.json"):
        self.file_path = Path(file_path)

    def load(self) -> dict:
        if not self.file_path.exists():
            return{}
        
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save(self, data: dict) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4) 