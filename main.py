"""
Основной модуль приложения Wallet API.

Содержит конфигурацию FastAPI приложения, маршруты и обработчики запросов.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.endpoints.wallets import router as wallets_router
from core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan менеджер для управления событиями жизненного цикла приложения.

    Выполняет создание таблиц в базе данных при старте приложения.
    """
    # Startup - выполняется при запуске приложения
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown - выполняется при остановке приложения
    # (можно добавить логику закрытия соединений при необходимости)


app = FastAPI(
    title="Wallet API",
    description="Система управления электронными кошельками с поддержкой операций пополнения и списания",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# Подключение маршрутов
app.include_router(wallets_router)


@app.get("/", summary="Корневой эндпоинт", description="Проверка работоспособности API")
async def root():
    """
    Корневой эндпоинт для проверки работы API.

    Returns:
        dict: Сообщение о статусе работы API
    """
    return {"message": "Wallet API is running"}


@app.get(
    "/health",
    summary="Проверка здоровья",
    description="Проверка статуса работы приложения и доступности сервисов",
)
async def health_check():
    """
    Эндпоинт для проверки здоровья приложения.

    Используется для мониторинга и проверки доступности сервиса.

    Returns:
        dict: Статус здоровья приложения
    """
    return {"status": "healthy"}


@app.get(
    "/info",
    summary="Информация о API",
    description="Получение основной информации о API",
)
async def api_info():
    """
    Предоставляет основную информацию о API.

    Returns:
        dict: Информация о версии и назначении API
    """
    return {
        "name": "Wallet API",
        "version": "1.0.0",
        "description": "Система управления электронными кошельками",
        "features": [
            "Создание кошельков",
            "Пополнение баланса",
            "Списание средств",
            "Просмотр баланса",
        ],
    }
