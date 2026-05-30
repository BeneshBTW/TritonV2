from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill


class FallbackSkill(BaseSkill):
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "general_chat"

    def execute(self, intent: Intent) -> Response:
        return Response(
            message=f"I heard you say: {intent.text}. I do not have a real AI brain connected yet.",
            success=True
        )