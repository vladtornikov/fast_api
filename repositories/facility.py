from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete, func

from src.repositories.base import BaseRepository
from src.models_database.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas_API.facilities import FacilityReply, RoomsFacilitiesReply, RoomsFacilitiesEdit
from src.repositories.utils import get_rooms_facilities

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    pydantic_schema = FacilityReply

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    pydantic_schema = RoomsFacilitiesReply

    async def edit_bulk(self, data_edit: BaseModel, exclude_unset: bool = False):
        if not data_edit.facility_id:
            return None

        get_facilities_id = await self.session.execute(
            get_rooms_facilities(data_edit.room_id)
        )
        current_facilities_id = set(*get_facilities_id.scalars().all())

        facilities_to_add = set(data_edit.facility_id) - current_facilities_id
        facilities_to_remove = current_facilities_id - set(data_edit.facility_id)

        if facilities_to_add:
            update_facilities = (
                insert(self.model)
                .values([
                    {'room_id': data_edit.room_id, 'facility_id': id_facility}
                    for id_facility in facilities_to_add
                    ])
            )
            print(update_facilities.compile(compile_kwargs={'literal_binds': True}))
            await self.session.execute(update_facilities)

        if facilities_to_remove:
            remove_facilities = (
                delete(self.model)
                .where(
                    RoomsFacilitiesORM.room_id == data_edit.room_id,
                    RoomsFacilitiesORM.facility_id.in_(facilities_to_remove)
                )
            )
            print(remove_facilities.compile(compile_kwargs={'literal_binds': True}))
            await self.session.execute(remove_facilities)

