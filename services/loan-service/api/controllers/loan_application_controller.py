from typing import Dict, List, Optional
from services.loan_application_service import LoanApplicationService
from api.dtos.loan_application_dto import LoanApplicationDTO

class LoanApplicationController:
    def __init__(self):
        self.service = LoanApplicationService()

    def create_application(self, user_id: str, data: Dict) -> Dict:
        result = self.service.submit_application(user_id, data)
        return LoanApplicationDTO.from_model(result).to_dict()

    def get_user_applications(self, user_id: str) -> List[Dict]:
        applications = self.service.get_user_applications(user_id)
        return [LoanApplicationDTO.from_model(app).to_dict() for app in applications]

    def get_application_detail(self, application_id: str) -> Optional[Dict]:
        application = self.service.get_application(application_id)
        if not application:
            return None
        return LoanApplicationDTO.from_model(application).to_dict()
