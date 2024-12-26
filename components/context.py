
import aiosqlite
from typing import Callable, Any
from collections.abc import Coroutine
from .UserState import UserState

class ApplicationContext:
    def __init__(self, database: Callable[[], Coroutine[Any, Any, aiosqlite.Connection]]):
        self._database_builder = database
        self._database = None
        self._UserStates : dict[int, UserState] = {}
    
    def get_user_state(self, id: int):
        if id not in self._UserStates:
            self._UserStates[id] = UserState()
        return self._UserStates[id]

    @property
    def database(self):
        if self._database is None:
            raise Exception('Context is not initialized')
        return self._database

    async def __aenter__(self):
        if self._database is None:
            self._database = await self._database_builder()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._database is not None:
            await self._database.close()
            self._database = None