import telegram.ext as tge
import telegram as tg
from collections.abc import Sequence, Coroutine
from typing import Callable, Any

from .context import ApplicationContext

import asyncio

class ApplicationComponent:
    def __init__(self, context: ApplicationContext):
        self._context = context
        self._handlers: list[tuple[tge.BaseHandler, int]] = []

    @property
    def handlers(self) -> Sequence[tuple[tge.BaseHandler, int]]:
        return self._handlers
    
    def add_handler(self, handler: tge.BaseHandler, group: int):
        self._handlers.append((handler, group))

    def wrap_callback(self, callback: Callable[[tg.Update, tge.ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]) -> Callable[[tg.Update, tge.ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]:
        async def wrapped_callback(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
            user_state = self._context.get_user_state(update.effective_user.id) #type: ignore
            
            this_interact = asyncio.get_running_loop().create_future()
            if user_state.current_interaction is not None:
                interact = user_state.current_interaction
                async def await_and_run():
                    try:
                        await interact
                        await callback(update, context)
                    finally:
                        this_interact.set_result(True)
                
                task = asyncio.get_running_loop().create_task(await_and_run())
            else:
                async def just_run():
                    try:
                        await callback(update, context)
                    finally:
                        this_interact.set_result(True)
                    
                task = asyncio.get_running_loop().create_task(just_run())
            user_state.current_interaction = this_interact
            await task

        return wrapped_callback