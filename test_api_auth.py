import pytest

from httpx import AsyncClient
from pydantic import EmailStr

from src.utils.database_cntxt_mngr import DBManager


@pytest.fixture
async def clean_cookies(ac: AsyncClient):
    ac.cookies.clear()
    return ac

@pytest.mark.parametrize('email, password, status_code', [
    ('rusbangkok@yandex.ru', '123456789', 200),
    ('rusphuket@gmail.com', 'anniehall1976', 200),
    ('rusphuket@.ru', 'anniehall1976', 422),
    ('', '', 422),
    ('rusbangkok@yandex.ru', '123456789', 409),
    ('rusphuket@gmail.com', 'anniehall1976', 409)
])
async def test_register_user(email: EmailStr, password: str, status_code: int, db: DBManager, ac: AsyncClient) -> None:
    response = await ac.post(
            '/auth/register',
            json={
                'email': email,
                'password': password
            }
        )
    assert response.status_code == status_code
    if response.status_code == 200:
        assert response.json()['status'] == 'OK'

@pytest.mark.parametrize('email, password, status_code', [
    ('rusphuket@gmail.ru', 'anniehall1976', 401),
    ('rusphuket@gmail.com', 'anniehall1976', 200),
    ('rusphuket@gmail.com', 'anniehall', 401)
])
async def test_login_and_get_user(clean_cookies, email: EmailStr, password: str, status_code: int,
                                  db: DBManager, ac: AsyncClient) -> None:
    response_login = await ac.post(
        '/auth/login',
        json={
            'email': email,
            'password': password
        }
    )
    assert response_login.status_code == status_code
    if response_login.status_code == 200:
        token = response_login.cookies.get('access_token')
        assert token

    response_me = await ac.get('/auth/me')
    assert response_me.status_code == status_code
    if response_me.status_code == 200:
        assert response_me.json()['email'] == email

async def test_delete_user(ac: AsyncClient):
    response = await ac.get('/auth/logout')
    assert response.status_code == 200
    assert 'access_token' not in response.cookies

async def test_get_unauthorized_user(db: DBManager, ac: AsyncClient):
    response = await ac.get('/auth/me')
    assert response.status_code == 401