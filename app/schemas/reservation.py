from typing import Optional
from pydantic import BaseModel, validator, root_validator, Extra, Field
from datetime import datetime, timedelta


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    """Базовый класс схемы"""

    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid
        # schema_extra = {
        #     'example': {
        #         'from_time': '2028-04-24T11:00',
        #         'to_time': '2028-04-24T12:00'
        #     }
        # }


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
    # Добавьте опциональное поле user_id.
    user_id: Optional[int]

    class Config:
        orm_mode = True
