from datetime import date

from pydantic import BaseModel
from sqlalchemy import select
from fastapi import HTTPException

from src.repositories.base import BaseRepository
from src.models_database.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BaseModel) -> BaseModel:
        available_rooms = rooms_ids_for_booking(date_from=data.date_from, date_to=data.date_to)
        available_rooms = await self.session.execute(available_rooms)
        available_rooms = available_rooms.scalars().all()
        res = list(filter(lambda x: data.room_id == x, available_rooms))
        if res:
            new_booking = await self.add(data)
            return new_booking
        raise HTTPException(status_code=401, detail='Данная комната уже забронирована')



