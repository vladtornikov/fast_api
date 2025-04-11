from httpx import AsyncClient
from fastapi import HTTPException

from src.utils.database_cntxt_mngr import DBManager



async def test_booking_add(db: DBManager, authenticated_ac: AsyncClient) -> None:
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        '/bookings',
        json={
            'room_id': room_id,
            'date_from': '2024-08-01',
            'date_to': '2024-08-10'
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res['status'] == 'OK'
    assert 'data' in res




