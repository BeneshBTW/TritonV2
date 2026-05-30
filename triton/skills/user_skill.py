from triton.core.intent import Intent
from triton.core.response import Response
from triton.core.session import SessionContext
from triton.skills.base_skill import BaseSkill

class UserSkill(BaseSkill):
    def __init__(self, session: SessionContext, user_memory_store):
        self.session = session
        self.user_memory_store = user_memory_store

    def can_handle(self, intent: Intent) -> bool:
        return intent.name in ["set_user_name", "get_user_name"]
    
    def execute(self, intent: Intent) -> Response:
        if intent.name == "set_user_name":
            self.session.user_name = intent.text

            self.user_memory_store.save({
                "user_name": self.session.user_name
            })

            return Response(
                message=f"Got it. Ill call you {self.session.user_name}",
                success=True
            )
        
        if self.session.user_name is None:
            return Response(
                message="I do not know your name yet.",
                success=True
            )
        
        return Response(
            message=f"Your name is {self.session.user_name}.",
            success=True
        )