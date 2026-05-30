from dataclasses import dataclass


@dataclass
class Response:
    message: str
    success: bool = True