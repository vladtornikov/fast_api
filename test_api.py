async def test_get_facilities(ac):
    response = await ac.get(
        '/facilities'
    )
    print(f'{response.json()=}')
    assert response.status_code == 200

async def test_add_facilites(ac):
    response = await ac.post(
        '/facilities',
        json={'title': 'унитаз с подогревом'}
    )
    print(f'{response.json()=}')
    assert response.status_code == 200