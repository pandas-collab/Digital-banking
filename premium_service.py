import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/premium_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoDeductionService:
    def __init__(self):
        self.schedule_file = 'auto_deduction_schedule.json'
        self.history_file = 'deduction_history.json'
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Create missing files with initial data"""
        for f in [self.schedule_file, self.history_file]:
            if not Path(f).exists():
                with open(f, 'w') as fp:
                    fp.write('[]')

    async def schedule_premium_deduction(self, policy_id: str, frequency_days: int, amount: float) -> Dict[str, Any]:
        """Schedule automatic premium deduction for a policy"""
        try:
            import json
            from uuid import uuid4

            # Validate inputs
            if not policy_id or frequency_days <= 0 or amount <= 0:
                raise ValueError("Invalid parameters")

            schedule = {
                'id': str(uuid4()),
                'policy_id': policy_id,
                'amount': float(amount),
                'frequency_days': int(frequency_days),
                'next_deduction': (datetime.now() + timedelta(days=frequency_days)).isoformat(),
                'status': 'active'
            }

            # Load existing schedule
            with open(self.schedule_file, 'r') as fp:
                schedules = json.load(fp)

            schedules.append(schedule)

            # Save updated schedule
            with open(self.schedule_file, 'w') as fp:
                json.dump(schedules, fp, indent=2)

            logger.info(f"Scheduled auto-deduction for policy {policy_id}: ${amount} every {frequency_days} days")
            return {"success": True, "schedule": schedule}

        except Exception as e:
            logger.error(f"Failed to schedule deduction: {str(e)}")
            return {"success": False, "error": str(e)}

    async def process_deductions(self) -> Dict[str, Any]:
        """Process all due deductions"""
        try:
            import json

            # Load schedules
            with open(self.schedule_file, 'r') as fp:
                schedules = json.load(fp)

            results = []
            now = datetime.now()

            for schedule in schedules:
                if schedule.get('status') == 'active':
                    next_ded = datetime.fromisoformat(schedule['next_deduction'])

                    if now >= next_ded:
                        # Process deduction
                        result = await self._deduct_premium(schedule)
                        if result['success']:
                            # Update schedule
                            schedule['next_deduction'] = (now + timedelta(days=schedule['frequency_days'])).isoformat()
                            results.append(f"Deducted ${schedule['amount']} from policy {schedule['policy_id']}")

                        # Save history
                        await self._save_deduction_history(schedule, result)

            # Save updated schedules
            with open(self.schedule_file, 'w') as fp:
                json.dump(schedules, fp, indent=2)

            logger.info(f"Processed {len(results)} deductions: {results}")
            return {"success": True, "processed": len(results), "results": results}

        except Exception as e:
            logger.error(f"Failed to process deductions: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _deduct_premium(self, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate premium deduction from account"""
        try:
            # In real implementation, integrate with banking system
            logger.info(f"Deducting ${schedule['amount']} from policy {schedule['policy_id']}")
            return {"success": True, "transaction_id": f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _save_deduction_history(self, schedule: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Save deduction history"""
        try:
            import json

            with open(self.history_file, 'r') as fp:
                history = json.load(fp)

            history.append({
                'policy_id': schedule['policy_id'],
                'amount': schedule['amount'],
                'date': datetime.now().isoformat(),
                'success': result['success'],
                'transaction_id': result.get('transaction_id', None)
            })

            with open(self.history_file, 'w') as fp:
                json.dump(history, fp, indent=2)

        except Exception as e:
            logger.error(f"Failed to save history: {str(e)}")

# FastAPI endpoint
async def setup_fastapi_endpoint():
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        app = FastAPI(title="Premium Auto-Deduction Service")
        service = AutoDeductionService()

        class ScheduleRequest(BaseModel):
            policy_id: str
            frequency_days: int
            amount: float

        @app.post("/api/schedule-premium")
        async def schedule_premium(request: ScheduleRequest):
            try:
                result = await service.schedule_premium_deduction(
                    request.policy_id,
                    request.frequency_days,
                    request.amount
                )
                if not result['success']:
                    raise HTTPException(status_code=400, detail=result['error'])
                return result
            except Exception as e:
                logger.error(f"Endpoint error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/process-deductions")
        async def process_deductions():
            try:
                result = await service.process_deductions()
                return result
            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return app

    except ImportError:
        logger.warning("FastAPI not installed, using CLI interface")
        return None

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Premium Auto-Deduction Service")
    parser.add_argument("--serve", action="store_true", help="Run FastAPI server")
    parser.add_argument("--schedule", nargs=3, metavar=("POLICY", "DAYS", "AMOUNT"),
                       help="Schedule auto-deduction")
    parser.add_argument("--process", action="store_true", help="Process due deductions")

    args = parser.parse_args()

    async def main():
        service = AutoDeductionService()

        if args.schedule:
            policy, days, amount = args.schedule
            result = await service.schedule_premium_deduction(policy, int(days), float(amount))
            print(json.dumps(result, indent=2))

        if args.process:
            result = await service.process_deductions()
            print(json.dumps(result, indent=2))

        if args.serve:
            app = await setup_fastapi_endpoint()
            if app:
                import uvicorn
                uvicorn.run(app, host="0.0.0.0", port=8000)
            else:
                print("Install fastapi: pip install fastapi uvicorn")
                sys.exit(1)

    if any([args.serve, args.schedule, args.process]):
        asyncio.run(main())
    else:
        print("Use --help for available commands")
