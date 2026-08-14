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
from triton.memory.task_store import TaskStore
from triton.skills.task_skill import TaskSkill
from triton.memory.reminder_store import ReminderStore
from triton.skills.reminder_skill import ReminderSkill
from triton.llm.ai_interpreter import AIInterpreter
from triton.services.task_service import TaskService
from triton.services.note_service import NoteService 
from triton.services.reminder_service import ReminderService
from triton.llm.ollama_interpreter import OllamaInterpreter


class Brain:
    def __init__(self):
        self.intent_parser = IntentParser()
        self.ai_interpreter = AIInterpreter()
        self.ollama_interpreter = OllamaInterpreter()
        self.user_memory_store = UserMemoryStore()
        self.note_service = NoteService(self.user_memory_store)
        self.task_store = TaskStore()
        self.task_service = TaskService(self.task_store)
        self.reminder_store = ReminderStore()
        self.reminder_service = ReminderService(self.reminder_store)
        saved_user_memory = self.user_memory_store.load()
        self.session = SessionContext()
        self.session.user_name = saved_user_memory.get("user_name")
        

        self.router = Router(
            skills=[
                BasicSkill(),
                TimeSkill(),
                SessionSkill(self.session),
                UserSkill(self.session, self.user_memory_store),
                NoteSkill(self.session, self.note_service),
                TaskSkill(self.session, self.task_service),
                ReminderSkill(self.session, self.reminder_service),
                FallbackSkill()
            ]
        )

    def process(self, user_input: str) -> Response:
        normalized_input = self.ai_interpreter.normalize(user_input)

        if normalized_input == user_input:
            print("using Ollama....")
            normalized_input = self.ollama_interpreter.normalize(user_input)

        intent = self.intent_parser.parse(normalized_input)

        self.session.record_turn(
            user_input=user_input,
            intent_name=intent.name
        )

        return self.router.route(intent)