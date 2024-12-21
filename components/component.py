import telegram.ext as tge
from collections.abc import Sequence

from .context import ApplicationContext

class ApplicationComponent:
    def __init__(self, context: ApplicationContext):
        self._context = context
        self._handlers: list[tuple[tge.BaseHandler, int]] = []

    @property
    def handlers(self) -> Sequence[tuple[tge.BaseHandler, int]]:
        return self._handlers