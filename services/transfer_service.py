import logging
from typing import List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from repositories.transfer import TransferRepository
from schemas.transfer_dto import TransferDto, PaginatedTransfersResponse
from models.transfer import Transfer

logger = logging.getLogger(__name__)

class TransferService:
    def __init__(self, db: Session):
        self.repository = TransferRepository(db)

    def get_user_transfers(self, user_id: str, page: int = 0, size: int = 10) -> Tuple[List[TransferDto], int]:
        """
        Get paginated transfers for user
        Args:
            user_id: UUID as string
            page: Zero-based page number
            size: Items per page
        Returns:
            Tuple of (list of TransferDto, total_pages)
        """
        try:
            # Validate UUID
            user_uuid = UUID(user_id)

            if page < 0:
                raise ValueError("Page must be non-negative")
            if size <= 0 or size > 100:
                raise ValueError("Size must be between 1 and 100")

            transfers, total_pages = self.repository.find_by_user_id(
                user_id=user_uuid,
                page=page,
                size=size
            )

            transfer_dtos = [
                TransferDto(
                    transferId=str(t.id),
                    fromAccountId=str(t.from_account_id),
                    toAccountId=str(t.to_account_id),
                    amount=float(t.amount),
                    createdAt=t.created_at.isoformat()
                )
                for t in transfers
            ]

            logger.debug(f"Retrieved {len(transfer_dtos)} transfers for user {user_id}, page {page}")

            return transfer_dtos, total_pages

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving transfers: {e}")
            raise
