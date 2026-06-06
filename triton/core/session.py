from dataclasses import dataclass, field


@dataclass
class SessionContext:
    user_name: str | None = None
    last_user_input: str = ""
    last_intent_name: str = ""
    turn_count: int = 0
    history: list[str] = field(default_factory=list)
    
    pending_action: str | None = None
    pending_data: dict | None = None

    last_undo_action: str | None = None
    last_undo_data: dict | None = None

    def record_turn(self, user_input: str, intent_name: str) -> None:
        self.last_user_input = user_input
        self.last_intent_name = intent_name
        self.turn_count += 1
        self.history.append(user_input)