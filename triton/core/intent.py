from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    text: str
    confidence: float = 1.0