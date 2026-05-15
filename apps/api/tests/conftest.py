"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool

from src.main import app
from src.database import get_session
from src.config import settings


TEST_DATABASE_URL = settings.database_url.replace(
    settings.database_url.split("/")[-1],
    "devora_test",
)


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncEngine:
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncClient:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()
