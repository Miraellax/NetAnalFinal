import telegram.ext as tge
from collections.abc import Sequence

from .context import ApplicationContext

class ApplicationComponent:
    def __init__(self, context: ApplicationContext):
        self._context = context
        self._handlers: list[tge.BaseHandler] = []

    @property
    def handlers(self) -> Sequence[tge.BaseHandler]:
        return self._handlers