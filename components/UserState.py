from collections.abc import Awaitable
from typing import Any

class UserState:
    def __init__(self):
        self.current_interaction : Awaitable | None = None
        self.current_action : str = ''
        self.dynamic_state : dict[str, Any] = {}