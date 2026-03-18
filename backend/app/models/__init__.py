from sqlalchemy.orm import declarative_base
Base = declarative_base()
from .user import User
from .account import Account
from .transfer import Transfer
from .loan import Loan
