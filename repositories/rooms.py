from datetime import date

from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.models_database.rooms import RoomsORM
from src.schemas_API.rooms import Room

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
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))
