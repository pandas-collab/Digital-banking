# Daily Premium Deduction Service

## Overview
This service implements a daily premium deduction mechanism similar to Spring's `@Scheduled` annotation.

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `python test_deduction.py`
3. Start service: `python main.py`

## Features
- Daily premium deductions at 00:00 UTC
- Defaulter marking on insufficient balance
- Comprehensive logging
- Health check endpoint
- Error handling and validation

## API Endpoints
- `GET /api/health` - Health check endpoint

## Environment Variables
- `DATABASE_URL` - Database connection string
- `PREMIUM_DEDUCTION_TIME` - Time of day for deductions (default: 00:00)
- `LOG_LEVEL` - Logging level (default: INFO)

## Testing
Run the test suite: `./setup_and_test.sh`
