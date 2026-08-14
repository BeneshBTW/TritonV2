import json
from pathlib import Path

class EventStore:
    def __init__(self, file_path: str = "triton/data/events.json"):
        self.file_path = Path(file_path)

    def load(self) -> list[dict]:
        if not self.file_path.exists():
            return []
        
        with open(self.file_path, "r") as file:
            return json.load(file)
        
    def save(self, events: list[dict]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w") as file:
            json.dump(events, file, indent=4)