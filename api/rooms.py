from fastapi import APIRouter, Body, Query
from datetime import date


from src.schemas_API.rooms import RoomsAddRequest, RoomsAdd, RoomsPatch, RoomsEdit, RoomsPatchNoFacilities
from src.schemas_API.facilities import RoomsFacilitiesAdd, RoomsFacilitiesEdit
from src.api.dependencies import DBDep

router = APIRouter(prefix='/hotels', tags=['Номера в отелях'])

@router.get(
    '/{hotel_id}/rooms',
    summary='Получение всех комнат в определенном отеле'
)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example='2024-08-01'),
        date_to: date = Query(example='2024-08-10')
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get(
    '/{hotel_id}/rooms/{room_id}',
    summary='Получение данных определенной комнаты'
)
async def get_data_about_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, room_id=room_id)

@router.delete(
    '/{hotels_id}/rooms/{room_id}',
    summary='Удаляем комнату из базы данных'
)
async def delete_room(db: DBDep,hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    return {'status': 'OK'}


@router.post(
    '/{hotel_id}/rooms',
    summary='Добавляем новые комнаты в определенный отель',
)
async def create_room(db: DBDep, hotel_id: int, room_data: RoomsAddRequest = Body):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {'status': 'OK', 'data': room}

@router.put(
    '/{hotel_id}/rooms/{room_id}',
    summary='Полное обновление данных о комнате',
    description='Нужно обязательно ввести все параметры'
)
async def update_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomsAddRequest = Body
):

    _room_data = RoomsEdit(**room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)

    room_facilities_edit = RoomsFacilitiesEdit(room_id=room_id, facility_id=room_data.facilities_ids)
    await db.rooms_facilities.edit_bulk(room_facilities_edit)
    await db.commit()
    return {'status': 'OK'}

@router.patch(
    '/{hotel_id}/rooms/{room_id}',
    summary='Частичное обновление данных о комнате',
    description='Необязательно передавать все параметры'
)
async def partially_update_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomsPatch = Body
):
    _room_data = RoomsPatchNoFacilities(**room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)

    room_facilities_edit = RoomsFacilitiesEdit(room_id=room_id, facility_id=room_data.facilities_ids)
    await db.rooms_facilities.edit_bulk(room_facilities_edit)
    await db.commit()
    return {'status': 'OK'}
