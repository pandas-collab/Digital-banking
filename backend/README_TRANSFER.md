# Transfer Functionality Documentation

## Overview
The transfer system enables users to transfer funds between accounts with built-in daily and monthly transfer limits.

## Daily & Monthly Limits
- **Daily Limit**: $50,000 USD (configurable per account)
- **Monthly Limit**: $500,000 USD (configurable per account)
- Limits reset at UTC midnight (daily) and UTC start of month (monthly)

## API Endpoints

### POST /api/v1/transfer
Transfer funds between accounts
