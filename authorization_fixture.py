@pytest.fixture(scope='session', autouse=True)
async def authenticated_ac(ac: httpx.AsyncClient, register_user):
    response = await ac.post(
        '/auth/login',
        json = {
            'email': 'kot@pes.com',
            'password': 'jack123@rambler.ru'
        }
    )
    assert response.status_code == 200
    token = response.cookies.get('access_token')
    assert token
    ac.headers.update({'Authorization': f'Bearer {token}'})
    return ac