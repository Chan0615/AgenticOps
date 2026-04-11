"""Shared async runner for Celery sync tasks."""

import asyncio

_CELERY_ASYNC_LOOP = None


def run_async(coro):
    """Run coroutine on a shared per-process event loop."""
    global _CELERY_ASYNC_LOOP
    if _CELERY_ASYNC_LOOP is None or _CELERY_ASYNC_LOOP.is_closed():
        _CELERY_ASYNC_LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(_CELERY_ASYNC_LOOP)
    return _CELERY_ASYNC_LOOP.run_until_complete(coro)
