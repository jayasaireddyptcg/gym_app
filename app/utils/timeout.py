import asyncio

async def with_timeout(coro, timeout=8):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return None
