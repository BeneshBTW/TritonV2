from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill

class Router:
    def __init__(self, skills: list[BaseSkill]):
        self.skills = skills

    def route(self, intent: Intent) -> Response:
        for skill in self.skills:
            if skill.can_handle(intent):
                return skill.execute(intent)
            
        return Response(
            message="I dont know how to handle that yet.",
            success=False
        )