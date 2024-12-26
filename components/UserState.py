from collections.abc import Awaitable
from typing import Any
import telegram as tg

class UserState:
    def __init__(self):
        self.current_interaction : Awaitable | None = None
        self.current_action : str = ''
        self.dynamic_state : dict[str, Any] = {}
        self.last_markup : tg.InlineKeyboardMarkup | tg.ReplyKeyboardMarkup | tg.ReplyKeyboardRemove | tg.ForceReply | None = None