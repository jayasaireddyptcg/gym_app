import asyncio

async def retry(func, retries=2, delay=1):
    for attempt in range(retries):
        try:
            return await func()
        except Exception:
            if attempt == retries - 1:
                return None
            await asyncio.sleep(delay)
