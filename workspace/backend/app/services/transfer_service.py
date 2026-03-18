import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.transfer_repository import TransferRepository
from backend.app.models.transfer import TransferRequest, TransferResponse
import logging

logger = logging.getLogger(__name__)

class TransferService:
    def __init__(self, db: AsyncSession):
        self.repository = TransferRepository(db)

    async def validate_daily_limit(self, from_account_id: str, amount: float) -> bool:
        """Validate if account can transfer without exceeding 500k daily limit."""
        account_uuid = uuid.UUID(from_account_id)
        daily_sum = await self.repository.get_daily_transfer_sum(account_uuid)

        total_after_transfer = daily_sum + amount
        limit_exceeded = total_after_transfer > 500000

        logger.info(
            f"Daily limit check for account {from_account_id}: "
            f"daily_sum={daily_sum}, amount={amount}, "
            f"total_after={total_after_transfer}, limit_exceeded={limit_exceeded}"
        )

        return not limit_exceeded

    async def create_transfer(self, transfer_request: TransferRequest) -> TransferResponse:
        """Process fund transfer with validation."""
        logger.info(f"Processing transfer request: {transfer_request}")

        # Validate UUID format
        try:
            from_account_uuid = uuid.UUID(transfer_request.fromAccount)
            to_account_uuid = uuid.UUID(transfer_request.toAccount)
        except ValueError:
            logger.error(f"Invalid UUID format in transfer request")
            raise ValueError("Invalid account ID format")

        # Check same account transfer
        if from_account_uuid == to_account_uuid:
            logger.error("Attempted self-transfer")
            raise ValueError("Cannot transfer to the same account")

        # Verify accounts exist
        from_exists = await self.repository.account_exists(from_account_uuid)
        to_exists = await self.repository.account_exists(to_account_uuid)

        if not from_exists:
            logger.error(f"Source account not found: {transfer_request.fromAccount}")
            raise ValueError("Source account not found")
        if not to_exists:
            logger.error(f"Destination account not found: {transfer_request.toAccount}")
            raise ValueError("Destination account not found")

        # Check sufficient funds
        balance = await self.repository.get_account_balance(from_account_uuid)
        if balance is None:
            logger.error(f"Could not retrieve balance for account {transfer_request.fromAccount}")
            raise ValueError("Could not validate account balance")

        if balance < transfer_request.amount:
            logger.error(
                f"Insufficient funds: balance={balance}, "
                f"requested={transfer_request.amount}"
            )
            raise ValueError("Insufficient funds")

        # Check daily limit
        can_transfer = await self.validate_daily_limit(
            transfer_request.fromAccount,
            transfer_request.amount
        )
        if not can_transfer:
            logger.error(f"Daily limit exceeded for account {transfer_request.fromAccount}")
            raise ValueError("Daily transfer limit exceeded")

        # Create transfer record
        transfer = await self.repository.create_transfer(
            from_account_uuid,
            to_account_uuid,
            transfer_request.amount
        )

        # Atomic transfer
        try:
            # Deduct from source
            new_from_balance = balance - transfer_request.amount
            await self.repository.update_account_balance(
                from_account_uuid,
                new_from_balance
            )
            logger.info(
                f"Deducted {transfer_request.amount} from "
                f"account {transfer_request.fromAccount}. New balance: {new_from_balance}"
            )

            # Credit to destination
            to_balance = await self.repository.get_account_balance(to_account_uuid)
            new_to_balance = to_balance + transfer_request.amount
            await self.repository.update_account_balance(
                to_account_uuid,
                new_to_balance
            )
            logger.info(
                f"Credited {transfer_request.amount} to "
                f"account {transfer_request.toAccount}. New balance: {new_to_balance}"
            )

            # Update transfer status
            await self.repository.update_transfer_status(
                uuid.UUID(transfer.id),
                "COMPLETED"
            )
            transfer.status = "COMPLETED"

        except Exception as e:
            logger.error(f"Transfer failed: {str(e)}")
            await self.repository.update_transfer_status(
                uuid.UUID(transfer.id),
                "FAILED"
            )
            transfer.status = "FAILED"
            raise

        logger.info(f"Transfer completed successfully: {transfer}")
        return transfer
