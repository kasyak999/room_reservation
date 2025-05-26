from sqlalchemy import Column, String, Text
from app.core.db import Base
from sqlalchemy.orm import relationship


class MeetingRoom(Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    name = Column(String(100), unique=True, nullable=False)
    # Новый атрибут модели. Значение nullable по умолчанию равно True,
    # поэтому его можно не указывать.
    description = Column(Text)
    reservations = relationship('Reservation', cascade='delete')
