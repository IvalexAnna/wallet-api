"""
API endpoints для управления кошельками.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.schemas.wallet_schemas import (
    OperationRequest,
    OperationResponse,
    WalletResponse,
)
from api.services.wallet_service import WalletService
from core.database import get_db

router = APIRouter(prefix="/api/v1", tags=["wallets"])


@router.get(
    "/wallets/{wallet_id}",
    response_model=WalletResponse,
    summary="Получить баланс кошелька",
    description="Получить текущий баланс указанного кошелька",
)
async def get_wallet_balance(wallet_id: str, db: Session = Depends(get_db)):
    """
    Получает баланс кошелька по его идентификатору.

    Args:
        wallet_id (str): Идентификатор кошелька
        db (Session): Сессия базы данных

    Returns:
        WalletResponse: Данные кошелька

    Raises:
        HTTPException: 404 если кошелек не найден
    """
    wallet = WalletService.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Кошелек не найден"
        )
    return WalletResponse(
        id=str(wallet.id),
        balance=float(wallet.balance),
        created_at=wallet.created_at.isoformat(),
        updated_at=wallet.updated_at.isoformat(),
    )


@router.post(
    "/wallets/{wallet_id}/operation",
    response_model=OperationResponse,
    summary="Выполнить операцию с кошельком",
    description="Выполнить операцию пополнения или списания средств",
)
async def wallet_operation(
    wallet_id: str, operation: OperationRequest, db: Session = Depends(get_db)
):
    """
    Выполняет операцию с кошельком (пополнение или списание).

    Args:
        wallet_id (str): Идентификатор кошелька
        operation (OperationRequest): Данные операции
        db (Session): Сессия базы данных

    Returns:
        OperationResponse: Результат операции

    Raises:
        HTTPException: 400 если операция не может быть выполнена
    """
    result = WalletService.perform_operation(db, wallet_id, operation)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"]
        )

    return OperationResponse(
        wallet_id=result["wallet_id"],
        operation_type=result["operation_type"],
        amount=result["amount"],
        new_balance=result["new_balance"],
        success=True,
    )


@router.post(
    "/wallets",
    response_model=WalletResponse,
    summary="Создать новый кошелек",
    description="Создает новый кошелек с нулевым балансом",
)
async def create_wallet(db: Session = Depends(get_db)):
    """
    Создает новый кошелек с нулевым балансом.

    Args:
        db (Session): Сессия базы данных

    Returns:
        WalletResponse: Данные созданного кошелька
    """
    wallet = WalletService.create_wallet(db)

    return WalletResponse(
        id=str(wallet.id),
        balance=float(wallet.balance),
        created_at=wallet.created_at.isoformat(),
        updated_at=wallet.updated_at.isoformat(),
    )
