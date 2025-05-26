from typing import Optional
from pydantic import BaseModel, validator, root_validator
from datetime import datetime


class ReservationBase(BaseModel):
    """Базовый класс схемы"""

    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                "Начало бронирования "
                "не может быть меньше текущего времени.")
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        from_reserve = values.get("from_reserve")
        to_reserve = values.get("to_reserve")
        if from_reserve >= to_reserve:
            raise ValueError(
                "Время окончания бронирования должно "
                "быть позже времени начала.")
        return values


class ReservationCreate(ReservationUpdate):
    """Схема для полученных данных."""
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        orm_mode = True
