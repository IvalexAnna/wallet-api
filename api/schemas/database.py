"""
Модели базы данных для кошельков.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base


class Wallet(Base):
    """
    Модель кошелька.

    Attributes:
        id (UUID): Уникальный идентификатор кошелька
        balance (Decimal): Баланс кошелька
        created_at (DateTime): Время создания кошелька
        updated_at (DateTime): Время последнего обновления
        version (int): Версия для оптимистичной блокировки
    """

    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(scale=2), nullable=False, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    version = Column(Numeric, default=1)

    def to_dict(self):
        """
        Преобразует объект кошелька в словарь.

        Returns:
            dict: Словарь с данными кошелька
        """
        return {
            "id": str(self.id),
            "balance": float(self.balance),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
