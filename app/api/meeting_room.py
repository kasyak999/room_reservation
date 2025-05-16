# app/api/meeting_room.py

from fastapi import APIRouter, HTTPException, Depends

from app.crud.meeting_room import create_meeting_room, get_room_id_by_name
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB
# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session

# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post(
    '/meeting_rooms/',
    # Указываем схему ответа.
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии, как параметр функции.
        session: AsyncSession = Depends(get_async_session),
):
    # Вызываем функцию проверки уникальности поля name:
    room_id = await get_room_id_by_name(meeting_room.name, session)
    # Если такой объект уже есть в базе - вызываем ошибку:
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )

    new_room = await create_meeting_room(meeting_room, session)
    return new_room
