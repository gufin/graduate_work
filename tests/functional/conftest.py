import asyncio
from dataclasses import dataclass
from uuid import UUID

import aiohttp
import pytest
from multidict import CIMultiDictProxy
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.entities import ProfileMovie
from settings import test_settings


@pytest.fixture(autouse=True)
async def setup_database():
    database_url = f'postgresql+asyncpg://{test_settings.user}:{test_settings.password}@{test_settings.db_host}:{test_settings.db_port}/{test_settings.db}'
    engine = create_async_engine(database_url)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        async with session.begin():
            await session.execute(text('TRUNCATE TABLE profiles CASCADE;'))
            await session.execute(text('TRUNCATE TABLE profile_movies CASCADE;'))
            await session.commit()


@pytest.fixture
async def create_test_movies():
    database_url = f'postgresql+asyncpg://{test_settings.user}:{test_settings.password}@{test_settings.db_host}:{test_settings.db_port}/{test_settings.db}'
    engine = create_async_engine(database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    test_profile_id = 'f970495e-a731-45f0-aa65-686bc6eada23'
    test_movies = [
        ProfileMovie(
            id=UUID('5c6d9a63-7e5a-4eaf-8331-72b1a7066ea1'),
            profile_id=test_profile_id,
            movie_id=UUID('805b3604-b770-46fe-9d25-5d24b4d3a0c2'),
        ),
        ProfileMovie(
            id=UUID('aaad87d0-9007-4a3c-a1f3-d4f9f9048b7c'),
            profile_id=test_profile_id,
            movie_id=UUID('4322cf42-5dea-43e8-92d4-27316e831b39'),
        ),
    ]

    async with async_session() as session:
        async with session.begin():
            for movie in test_movies:
                session.add(movie)
            await session.commit()


@pytest.fixture
async def create_profile(make_post_request):
    await make_post_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23',
        params={
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'patronymic': 'TestPatronymic',
            'phone': '+1234567890',
        },
    )


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = f'{test_settings.service_api_url}{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = f'{test_settings.service_api_url}{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner


@pytest.fixture
def make_put_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = f'{test_settings.service_api_url}{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner


@pytest.fixture
def make_delete_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = f'{test_settings.service_api_url}{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner
