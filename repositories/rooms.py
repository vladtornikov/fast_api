from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import Any
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models_database.rooms import RoomsORM
from src.models_database.facilities import RoomsFacilitiesORM
from src.schemas_API.rooms import Room, RoomWithRels

class RoomsRepository(BaseRepository):
    model = RoomsORM
    pydantic_schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_hotel_with_facilities(self, **filter_by: Any) -> BaseModel:
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return RoomWithRels.model_validate(model, from_attributes=True)


