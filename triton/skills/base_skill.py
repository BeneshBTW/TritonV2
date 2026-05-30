from abc import ABC, abstractmethod
from triton.core.intent import Intent
from triton.core.response import Response

class BaseSkill(ABC):
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        pass

    @abstractmethod
    def execute(self, intent: Intent) -> Response:
        pass