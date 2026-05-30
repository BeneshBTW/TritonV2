from datetime import datetime

from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill

class TimeSkill(BaseSkill):
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "get_time"
    
    def execute(self, intent: Intent) -> Response:
        current_time = datetime.now().strftime("%I:%M %p")

        return Response(
            message=f"The current time is {current_time}.",
            success=True
        )