from datetime import date

from src.database import BaseORM
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Integer


class BookingsORM(BaseORM):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    date_from: Mapped[date] = mapped_column(DateTime)
    date_to: Mapped[date] =mapped_column(DateTime)
    price: Mapped[int] =mapped_column(Integer)

    @property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
