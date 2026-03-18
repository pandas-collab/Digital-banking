from typing import List, Optional
from abc import ABC, abstractmethod
from domain.models.loan_application import LoanApplication

class LoanApplicationRepository(ABC):
    @abstractmethod
    def create(self, application: LoanApplication) -> LoanApplication:
        pass

    @abstractmethod
    def get_by_id(self, application_id: str) -> Optional[LoanApplication]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[LoanApplication]:
        pass

    @abstractmethod
    def update(self, application: LoanApplication) -> LoanApplication:
        pass

    @abstractmethod
    def get_all(self, limit: int = 100, offset: int = 0) -> List[LoanApplication]:
        pass
