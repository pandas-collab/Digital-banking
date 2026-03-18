import asyncio
import sys
from main import PremiumDeductionService

async def test_daily_premium_deduction():
    """Test the daily premium deduction service"""
    service = PremiumDeductionService()

    print("Testing daily premium deduction...")
    result = await service.deduct_premiums()

    if result:
        print(" Test passed: Premium deduction completed successfully")
        return 0
    else:
        print(" Test failed: Premium deduction failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_daily_premium_deduction())
    sys.exit(exit_code)
