import pytest
import json

from src.config import settings
from src.database import BaseORM, engine_null_pool
from src.main import app
from src.models_database import *
from httpx import ASGITransport, AsyncClient
from src.schemas_API.hotels import HotelADD


@pytest.fixture(scope='session', autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def add_hotels_and_rooms(setup_database):
    print('hello')
    with open('tests/mock_hotels.json', encoding='utf-8') as hotels:
        hotels_deserial: list[dict] = json.load(hotels)

    with open('tests/mock_rooms.json', encoding='utf-8') as rooms:
        rooms_deserial: list[dict] = json.load(rooms)

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        for hotel in hotels_deserial:
            response = await ac.post('/hotels', json=hotel)
            print(response)

        for room in rooms_deserial:
            response = await ac.post(f'/hotels/{room["hotel_id"]}/rooms', json=room)
            print(response)

@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        await ac.post(
            '/auth/register',
            json = {
                'email': 'kot@pes.com',
                'password': 'jack123@rambler.ru'
            }
        )