# app/api/meeting_room.py

from fastapi import APIRouter, HTTPException, Depends

from app.crud.meeting_room import (
    create_meeting_room, get_room_id_by_name, read_all_rooms_from_db,
    get_meeting_room_by_id, update_meeting_room, delete_meeting_room)
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate)
# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session

# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем модель, чтобы указать её в аннотации.
from app.models.meeting_room import MeetingRoom

# router = APIRouter()
# Добавьте параметр prefix.
router = APIRouter(prefix='/meeting_rooms', tags=['Meeting Rooms'])


@router.post(
    '/',
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
    # room_id = await get_room_id_by_name(meeting_room.name, session)
    # # Если такой объект уже есть в базе - вызываем ошибку:
    # if room_id is not None:
    #     raise HTTPException(
    #         status_code=422,
    #         detail='Переговорка с таким именем уже существует!',
    #     )

    # new_room = await create_meeting_room(meeting_room, session)
    # return new_room

    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    # Оставьте только закрывающий слеш.
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    return await read_all_rooms_from_db(session)


# --------------------------------------------------
@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Получаем объект из БД по ID.
    # В ответ ожидается либо None, либо объект класса MeetingRoom.
    meeting_room = await get_meeting_room_by_id(
        meeting_room_id, session
    )

    # if meeting_room is None:
    #     raise HTTPException(
    #         # Для отсутствующего объекта вернем статус 404 — Not found.
    #         status_code=404,
    #         detail='Переговорка не найдена!'
    #     )
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаём в корутину все необходимые для обновления данные.
    meeting_room = await update_meeting_room(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await delete_meeting_room(
        meeting_room, session
    )
    return meeting_room


# Корутина, проверяющая уникальность полученного имени переговорки.
async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


# Оформляем повторяющийся код в виде отдельной корутины.
async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    meeting_room = await get_meeting_room_by_id(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room
