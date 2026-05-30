from triton.core.intent_parser import IntentParser
from triton.core.response import Response
from triton.core.router import Router
from triton.skills.basic_skill import BasicSkill
from triton.skills.fallback_skill import FallbackSkill
from triton.skills.time_skill import TimeSkill
from triton.core.session import SessionContext
from triton.skills.session_skill import SessionSkill
from triton.skills.user_skill import UserSkill
from triton.memory.user_memory_store import UserMemoryStore
from triton.skills.note_skill import NoteSkill


class Brain:
    def __init__(self):
        self.intent_parser = IntentParser()
        self.user_memory_store = UserMemoryStore()
        saved_user_memory = self.user_memory_store.load()
        self.session = SessionContext()
        self.session.user_name = saved_user_memory.get("user_name")

        self.router = Router(
            skills=[
                BasicSkill(),
                TimeSkill(),
                SessionSkill(self.session),
                UserSkill(self.session, self.user_memory_store),
                NoteSkill(self.session, self.user_memory_store),
                FallbackSkill()
            ]
        )

    def process(self, user_input: str) -> Response:
        intent = self.intent_parser.parse(user_input)

        self.session.record_turn(
            user_input=user_input,
            intent_name=intent.name
        )

        return self.router.route(intent)