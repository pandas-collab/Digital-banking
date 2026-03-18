
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from api.database import SessionLocal
from models.transfer import Transfer

def create_sample_transfers():
    db: Session = SessionLocal()

    user_id = uuid.UUID('a1b2c3d4-e5f6-7890-abcd-1234567890ab')

    # Clear existing
    db.query(Transfer).delete()

    # Create 15 sample transfers
    transfers = []
    for i in range(15):
        transfer = Transfer(
            id=uuid.uuid4(),
            user_id=user_id,
            from_account_id=uuid.uuid4(),
            to_account_id=uuid.uuid4(),
            amount=100 * (i + 1),
            created_at=datetime.utcnow() - timedelta(days=i)
        )
        transfers.append(transfer)

    db.add_all(transfers)
    db.commit()
    db.close()

    print(f"Created 15 sample transfers for user {user_id}")

if __name__ == "__main__":
    create_sample_transfers()
