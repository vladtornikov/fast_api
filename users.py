from pydantic import EmailStr, BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.exceptions import EmailAlreadyExistsException, ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models_database.users import UsersORM
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas_API.users import UserAdd, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> BaseModel:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)

    async def register_user(self, data: UserAdd) -> BaseModel:
        try:
            return await self.add(data)
        except ObjectNotFoundException:
            raise EmailAlreadyExistsException



