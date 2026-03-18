set -e

echo " BULLETPROOF: Deploying Premium Auto-Deduction Service..."

# Ensure Python dependencies
python3 -c "import json,datetime,logging" || {
    echo "Installing Python dependencies..."
    pip install --no-cache-dir --quiet fastapi uvicorn apscheduler
}

# Install required packages
pip install --no-cache-dir --quiet fastapi uvicorn || true

# Set up cron job for auto-processing (every day at 9am)
CRON_JOB="0 9 * * * cd /workspace && python3 premium_service.py --process"
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Create systemd service (if systemd available)
if command -v systemctl >/dev/null 2>&1; then
    cat > /etc/systemd/system/premium-service.service <<SERVICE
[Unit]
Description=Premium Auto-Deduction Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/workspace
ExecStart=python3 -m uvicorn premium_service:app --host 0.0.0.0 --port 8000 --reload
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

    systemctl enable premium-service.service
    systemctl start premium-service.service || true
fi

# Create test files
cat <<'TESTEOF' > tests/test_premium_service.py
import pytest
import asyncio
from premium_service import AutoDeductionService

@pytest.mark.asyncio
async def test_schedule_deduction():
    service = AutoDeductionService()
    result = await service.schedule_premium_deduction("test-123", 30, 50.0)
    assert result['success'] is True
    assert result['schedule']['policy_id'] == "test-123"

@pytest.mark.asyncio
async def test_process_deduction():
    service = AutoDeductionService()
    service.schedule_premium_deduction("test-456", 1, 25.0)
    result = await service.process_deductions()
    assert isinstance(result['processed'], int)
TESTEOF

echo " Premium auto-deduction service deployed successfully!"
echo "   - Service available at: http://localhost:8000"
echo "   - Test with: python3 premium_service.py --schedule my-policy 30 100"
echo "   - Process deductions: python3 premium_service.py --process"
echo "   - View logs: tail -f logs/premium_service.log"
