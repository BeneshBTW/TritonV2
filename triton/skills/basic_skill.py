from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill


class BasicSkill(BaseSkill):
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "greeting"

    def execute(self, intent: Intent) -> Response:
        return Response(
            message="Hello. Triton is online.",
            success=True
        )