import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from api.schemas.database import Wallet
from api.schemas.wallet_schemas import OperationRequest, OperationType


class WalletService:
    @staticmethod
    def get_wallet(db: Session, wallet_id: str) -> Optional[Wallet]:
        """Получить кошелек по ID"""
        try:
            wallet_uuid = uuid.UUID(wallet_id)
        except ValueError:
            return None

        stmt = select(Wallet).where(Wallet.id == wallet_uuid)
        wallet = db.execute(stmt).scalar_one_or_none()
        return wallet

    @staticmethod
    def create_wallet(db: Session) -> Wallet:
        """Создать новый кошелек"""
        wallet = Wallet(balance=Decimal("0.00"))
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet

    @staticmethod
    def perform_operation(
        db: Session, wallet_id: str, operation: OperationRequest
    ) -> dict:
        """Выполнить операцию DEPOSIT/WITHDRAW с оптимистичной блокировкой"""
        try:
            wallet_uuid = uuid.UUID(wallet_id)
        except ValueError:
            return {"success": False, "error": "Invalid wallet ID"}

        max_retries = 3
        for attempt in range(max_retries):
            try:
                wallet = WalletService.get_wallet(db, wallet_id)
                if not wallet:
                    return {"success": False, "error": "Wallet not found"}

                current_balance = Decimal(str(wallet.balance))
                operation_amount = Decimal(str(operation.amount))

                if operation.operation_type == OperationType.DEPOSIT:
                    new_balance = current_balance + operation_amount
                elif operation.operation_type == OperationType.WITHDRAW:
                    if current_balance < operation_amount:
                        return {
                            "success": False,
                            "error": "Insufficient funds",
                            "current_balance": float(current_balance),
                            "requested_amount": float(operation_amount),
                        }
                    new_balance = current_balance - operation_amount
                else:
                    return {"success": False, "error": "Invalid operation type"}
                stmt = (
                    update(Wallet)
                    .where(Wallet.id == wallet_uuid, Wallet.version == wallet.version)
                    .values(balance=new_balance, version=Wallet.version + 1)
                )

                result = db.execute(stmt)
                db.commit()

                if result.rowcount == 0:
                    if attempt < max_retries - 1:
                        db.rollback()
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "Operation failed due to concurrent modification",
                        }
                updated_wallet = WalletService.get_wallet(db, wallet_id)

                return {
                    "success": True,
                    "wallet_id": wallet_id,
                    "operation_type": operation.operation_type,
                    "amount": float(operation_amount),
                    "new_balance": float(updated_wallet.balance),
                    "wallet": updated_wallet,
                }

            except Exception as e:
                db.rollback()
                if attempt == max_retries - 1:
                    return {"success": False, "error": f"Operation failed: {str(e)}"}

        return {"success": False, "error": "Max retries exceeded"}
