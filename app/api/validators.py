from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
# Так как в Python-пакете app.models модели импортированы в __init__.py,
# импортировать их можно прямо из пакета.
from app.models import MeetingRoom, Reservation


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    # Замените вызов функции на вызов метода.
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room


async def check_reservation_intersections(**kwargs) -> None:
    """Пповерка переговорки"""
    reservations = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )
    return None


async def check_reservation_before_edit(
    reservation_id: int,
    session: AsyncSession
) -> Reservation:
    reservation = await reservation_crud.get(reservation_id, session)
    if not reservation:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!'
        )
    return reservation
