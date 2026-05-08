from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis

from .config import settings

# Redis connection
redis_client = redis.from_url(settings.redis_url)


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Dependency to get Redis client."""
    async with redis_client as client:
        try:
            yield client
        finally:
            await client.close()


@asynccontextmanager
async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis client for use in services."""
    async with redis_client as client:
        try:
            yield client
        finally:
            await client.close()
