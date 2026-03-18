import logging
from ledger_service_fixed import BulletproofLedgerService
from cashflow_event import CashFlowEvent

# Initialize bulletproof ledger
logger = logging.getLogger(__name__)
ledger_service = BulletproofLedgerService()

def record_cashflow_event(event_type, account_id, amount, prev_balance, new_balance, metadata=None):
    """External interface for 100% cash-flow transparency"""
    try:
        event = CashFlowEvent(event_type, account_id, amount, prev_balance, new_balance, metadata)
        success = ledger_service.record_event(event)
        if success:
            logger.info(f"Cashflow recorded: {event.event_type} for {account_id}")
        return success
    except Exception as e:
        logger.error(f"Failed to record cashflow: {e}")
        return False
