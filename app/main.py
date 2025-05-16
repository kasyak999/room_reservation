from fastapi import FastAPI
# Импортируем настройки проекта из config.py.
from app.core.config import settings
from app.api.meeting_room import router

# Устанавливаем заголовок приложения при помощи аргумента title,
# в качестве значения указываем атрибут app_title объекта settings.
app = FastAPI(title=settings.app_title, description=settings.description)

# Подключаем роутер.
app.include_router(router)
