from settings import test_settings
import asyncio
import os
from dataclasses import dataclass

import aiohttp
import pytest
from dotenv import load_dotenv
from multidict import CIMultiDictProxy
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int

@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "my-app/0.0.1",
            "Test": "1",
        }
        url = f"{test_settings.service_api_url}{endpoint}"
        async with aiohttp.ClientSession(headers=headers) as session:
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
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "my-app/0.0.1",
            "Test": "1",
        }
        url = f"{test_settings.service_api_url}{endpoint}"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner
