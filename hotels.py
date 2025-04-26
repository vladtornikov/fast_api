from fastapi import APIRouter, Body, Query, HTTPException
from datetime import date

from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.schemas_API.hotels import HotelADD, HotelPatch
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get(
    '',
    summary='Тут мы получаем данные об отеле',
    description='Если ввести id, name или (и) title, то получим данные о конкретном отеле'
)
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
        date_from: date = Query(example="2025-02-10"),
        date_to: date = Query(example="2025-02-15")
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail='Дата заезда должна быть раньше даты выезда')
    return await db.hotels.get_filtered_by_time(
        title=title,
        location=location,
        date_from=date_from,
        date_to=date_to,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page
    )


@router.get(
    '/{hotel_id}',
    summary='Тут мы получаем один отель по его айди'
)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        res = await db.hotels.get_one(id=hotel_id)
        return res
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail='Отель не найден')

@router.delete(
    "/{hotel_id}",
    summary='Тут мы удаляем отель'
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"status": "OK"}

@router.post(
    '',
    summary='Тут мы можем добавить данные о новом отеле'
)
async def create_hotel(db: DBDep, hotel_data: HotelADD = Body(openapi_examples={
    "1": {
        "summary": "Бангкок",
        "value": {
            "title": "Отель Амара Бангкок",
            "location": "Бангкок, Суравонг, 10500",
        }
    },
    "2": {
        "summary": "Москва",
        "value": {
            "title": "Рэдиссон Славянская",
            "location": "Площадь трех вокзалов, 3",
        }
    }
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}

@router.put(
    "/{hotel_id}",
    summary='Обновление данных об отеле',
    description='Тут мы полностью обновляем данные об отеле: нужно обязательно передать и name, и title'
)
async def change_whole_hotel(db: DBDep, hotel_data: HotelADD, hotel_id: int):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить title, а можно location",
)
async def partially_change_hotel(db: DBDep, hotel_id:int, hotel_data: HotelPatch = Body):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


