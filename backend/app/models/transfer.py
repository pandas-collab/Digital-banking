from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship
from . import Base

class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"))
    to_account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Numeric(10, 2))
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])
