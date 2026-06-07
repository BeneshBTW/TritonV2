from dataclasses import dataclass, field


@dataclass
class Intent:
    name: str
    text: str
    confidence: float = 1.0
    data: dict = field(default_factory=dict)