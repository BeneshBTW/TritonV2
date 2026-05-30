from triton.core.intent import Intent
from triton.core.response import Response
from triton.core.session import SessionContext
from triton.skills.base_skill import BaseSkill


class SessionSkill(BaseSkill):
    def __init__(self, session: SessionContext):
        self.session = session

    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "session_recall"

    def execute(self, intent: Intent) -> Response:
        if self.session.turn_count <= 1:
            return Response(
                message="You have not said anything before this yet.",
                success=True
            )

        previous_input = self.session.history[-2]

        return Response(
            message=f"You just said: {previous_input}",
            success=True
        )