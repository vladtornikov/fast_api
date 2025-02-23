from pydantic import BaseModel

class FacilityRequest(BaseModel):
    title: str

class FacilityReply(FacilityRequest):
    id: int

class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomsFacilitiesReply(BaseModel):
    id: int

class RoomsFacilitiesEdit(BaseModel):
    room_id: int
    facility_id: list[int] | list = list



