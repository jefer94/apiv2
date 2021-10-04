"""
This mixin pretend provide multiple mixin to manage async code in a sync context
"""
import asyncio


class RunAsSyncMixin:
    def run_as_sync(self, async_func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        coroutine = async_func(*args, **kwargs)
        asyncio.run(coroutine)
        loop.run_until_complete(coroutine)
        return coroutine
