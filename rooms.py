from pydantic import BaseModel, Field


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

class Room(RoomsAdd):
    id: int

class RoomsEdit(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomsPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = Field(None)

class RoomsPatchNoFacilities(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)