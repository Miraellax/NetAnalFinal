from .context import ApplicationContext
from .component import ApplicationComponent
import telegram.ext as tge
from typing import Callable

import asyncio

class ApplicationCore:
    def __init__(self, context: Callable[[], ApplicationContext], bot_token: str):
        self._context = context
        self._token = bot_token
        self._components : list[Callable[[ApplicationContext], ApplicationComponent]] = []

    def add_component(self, component: Callable[[ApplicationContext], ApplicationComponent]):
        self._components.append(component)

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        bot_app = tge.ApplicationBuilder().token(self._token).build()
        async with self._context() as context:
            components = [
                component(context)
                for component in self._components
            ]
            for component in components:
                for handler, group in component.handlers:
                    bot_app.add_handler(handler, group)
            await bot_app.initialize()
            await bot_app.start()
            await bot_app.updater.start_polling() #type: ignore
            try:
                await asyncio.Future()
            finally:
                await bot_app.updater.stop() #type: ignore
                await bot_app.stop()
                await bot_app.shutdown()
