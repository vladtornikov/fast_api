import pytest


from httpx import AsyncClient
from typing import Callable


from src.utils.database_cntxt_mngr import DBManager
from tests.conftest import db_null_pool


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 500),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_booking_add(room_id: int, date_from: str, date_to: str, status_code: int,
                           db: DBManager, authenticated_ac: AsyncClient) -> None:
    response = await authenticated_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res['status'] == 'OK'
        assert 'data' in res



@pytest.fixture(scope='module')
async def delete_all_bookings():
    async for _db in db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize('room_id, date_from, date_to, bookings_amount', [
    (3, '2025-04-16', '2025-04-20', 1),
    (3, '2025-04-17', '2025-04-21', 2),
    (3, '2025-04-18', '2025-04-22', 3)
])
async def test_add_and_get_bookings(delete_all_bookings,
                                    room_id: int, date_from: str, date_to: str, bookings_amount: int,
                                    db: DBManager, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(
        '/bookings',
        json = {
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res['status'] == 'OK'
    assert 'data' in res

    response_to_get = await authenticated_ac.get(
        '/bookings'
    )
    assert response_to_get.status_code == 200
    res = response_to_get.json()
    assert len(res['data']) == bookings_amount










