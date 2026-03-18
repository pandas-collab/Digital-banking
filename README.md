# Insurance Purchase System

## Quick Setup
1. Install dependencies:
   - Node.js 16+
   - Python 3.8+
   - Docker & Docker-compose

### Frontend Setup
1. Install dependencies: `npm install`
2. Start development server: `npm run dev`
3. Build for production: `npm run build`

### Backend Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `python test_deduction.py`
3. Build: The service is ready to run after dependency installation
4. Start: `python main.py`

### Docker Setup
1. Start all services: `docker-compose up -d`
2. View logs: `docker-compose logs -f`
3. Stop all services: `docker-compose down`

### Post-merge process
After merging, run: `./setup_and_test.sh`

## Services Architecture
- **Frontend**: Next.js React app
- **Backend**: Python Flask REST API
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ

## Environment Variables
- `DATABASE_URL` - Database connection string
- `PREMIUM_DEDUCTION_TIME` - Time of day for deductions (default: 00:00)
- `LOG_LEVEL` - Logging level (default: INFO)
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `RABBITMQ_URL` - Message queue connection string
- `PORT` - Backend server port (default: 5000)

## API Endpoints
- `GET /api/health` - Health check endpoint
- `POST /api/auth/login` - User authentication
- `GET /api/policies` - List user's policies
- `POST /api/policies/buy` - Purchase new policy
- `GET /api/premiums/deductions` - Get premium deduction history

## Features
- Daily premium deductions at 00:00 UTC
- Defaulter marking on insufficient balance
- Comprehensive logging
- Health check endpoint
- Error handling and validation
- Transaction management
- User authentication & authorization

## Testing
Run the test suite: `./setup_and_test.sh`
