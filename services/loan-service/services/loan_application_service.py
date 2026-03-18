from typing import List, Optional
from decimal import Decimal
from domain.models.loan_application import LoanApplication
from infrastructure.repositories.postgres_loan_repository import PostgresLoanApplicationRepository
from services.credit_check_service import CreditCheckService
from services.risk_assessment_service import RiskAssessmentService
from services.notification_service import NotificationService

class LoanApplicationService:
    def __init__(self):
        self.repository = PostgresLoanApplicationRepository()
        self.credit_service = CreditCheckService()
        self.risk_service = RiskAssessmentService()
        self.notification_service = NotificationService()

    def submit_application(self, user_id: str, data: dict) -> LoanApplication:
        application = LoanApplication(
            user_id=user_id,
            amount=Decimal(str(data['amount'])),
            term_months=data['term_months'],
            interest_rate=self._calculate_interest_rate(data['term_months'], data.get('credit_score', 0)),
            purpose=data['purpose'],
            annual_income=Decimal(str(data['annual_income'])),
            employment_status=data['employment_status'],
            credit_score=data.get('credit_score')
        )

        validated_application = self._validate_application(application)
        saved_application = self.repository.create(validated_application)

        # Trigger initial assessment
        self._process_initial_assessment(saved_application)

        self.notification_service.notify_status_change(
            user_id=user_id,
            application_id=saved_application.id,
            status="submitted"
        )

        return saved_application

    def get_user_applications(self, user_id: str) -> List[LoanApplication]:
        return self.repository.get_by_user_id(user_id)

    def get_application(self, application_id: str) -> Optional[LoanApplication]:
        return self.repository.get_by_id(application_id)

    def _calculate_interest_rate(self, term_months: int, credit_score: int) -> Decimal:
        base_rate = Decimal('0.05')
        credit_modifier = Decimal('0.00')

        if credit_score >= 750:
            credit_modifier = Decimal('-0.005')
        elif credit_score >= 650:
            credit_modifier = Decimal('0.005')
        elif credit_score >= 550:
            credit_modifier = Decimal('0.015')
        else:
            credit_modifier = Decimal('0.025')

        term_modifier = (Decimal(str(term_months)) / Decimal('12')) * Decimal('0.004')

        return base_rate + credit_modifier + term_modifier

    def _validate_application(self, application: LoanApplication) -> LoanApplication:
        if application.amount <= Decimal('0'):
            raise ValueError("Loan amount must be positive")

        if application.term_months < 12 or application.term_months > 360:
            raise ValueError("Loan term must be between 12 and 360 months")

        if application.annual_income < Decimal('20000'):
            raise ValueError("Annual income must be at least $20,000")

        return application

    def _process_initial_assessment(self, application: LoanApplication):
        credit_report = self.credit_service.get_credit_report(application.user_id)
        risk_score = self.risk_service.evaluate_risk(application, credit_report)

        # Update application with initial assessment
        application.status = "under_review"
        application.credit_score = credit_report.score
        self.repository.update(application)
