"""
Pydantic схемы для валидации данных кошельков.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OperationType(str, Enum):
    """Типы операций с кошельком."""

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletResponse(BaseModel):
    """
    Схема ответа с данными кошелька.

    Attributes:
        id (str): Идентификатор кошелька
        balance (float): Текущий баланс
        created_at (str): Время создания в ISO формате
        updated_at (str): Время обновления в ISO формате
    """

    id: str
    balance: float
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class OperationRequest(BaseModel):
    """
    Схема запроса на операцию с кошельком.

    Attributes:
        operation_type (OperationType): Тип операции
        amount (float): Сумма операции (должна быть больше 0)
    """

    operation_type: OperationType
    amount: float = Field(gt=0, description="Сумма должна быть больше 0")


class OperationResponse(BaseModel):
    """
    Схема ответа на операцию с кошельком.

    Attributes:
        wallet_id (str): Идентификатор кошелька
        operation_type (OperationType): Тип выполненной операции
        amount (float): Сумма операции
        new_balance (float): Новый баланс после операции
        success (bool): Флаг успешности операции
    """

    wallet_id: str
    operation_type: OperationType
    amount: float
    new_balance: float
    success: bool
