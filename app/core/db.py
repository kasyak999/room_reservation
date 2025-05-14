# Все классы и функции для асинхронной работы
# находятся в модуле sqlalchemy.ext.asyncio.
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy import Column, Integer
from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

# async_session = AsyncSession(engine)  # создаётся только один объект сессии,
# а для работы асинхронного приложения потребуется постоянно открывать и
# закрывать сессии: для каждого запроса — своя сессия.

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
