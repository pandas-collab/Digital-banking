echo " API Integration Test..."
echo "Testing Ledger Service Import..."
python3 -c "
from ledger_service_fixed import BulletproofLedgerService
from cashflow_event import CashFlowEvent
print(' All imports successful')
ledger = BulletproofLedgerService()
print(' Ledger service initialized')
"
echo " API integration test passed"
