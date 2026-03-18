# Core Banking Platform – Account Transfer System

## Quick Setup
### All-in-one
1. Start all services: `docker-compose up -d`
2. Initialize database migrations & seed data:
   ```bash
   cd backend && alembic upgrade head
   python -c "from app.main import app; from app.models import Base, engine; Base.metadata.create_all(engine)"
   ```
3. Run full test & build suite: `./setup_and_test.sh`

### Frontend Setup (Insurance & Account UIs)
1. Install dependencies:  
   `cd frontend && npm install`
2. Start development server:  
   `npm run dev`
3. Build for production:  
   `npm run build`

### Backend Setup (Transfer service + legacy insurance APIs)
1. Install dependencies:  
   `pip install -r requirements.txt`
2. Run tests:  
   `cd backend && pytest`
3. Start service:  
   `python main.py`

### Docker-only (no local toolchain)
1. Start everything: `docker-compose up -d`
2. View logs: `docker-compose logs -f`
3. Stop everything: `docker-compose down`

## Services Architecture
- **Frontend**: Next.js React app  
- **Backend**: Python Flask REST APIs (legacy insurance + new transfer engine)  
- **Database**: PostgreSQL  
- **Cache**: Redis  
- **Message Queue**: RabbitMQ  

## Environment Variables
- `DATABASE_URL` – PostgreSQL connection string  
- `PREMIUM_DEDUCTION_TIME` – UTC time for daily deductions (default: `00:00`)  
- `LOG_LEVEL` – Logging level (default: `INFO`)  
- `REDIS_URL` – Redis connection string  
- `JWT_SECRET` – Secret key for JWT tokens  
- `RABBITMQ_URL` – Message queue connection string  
- `PORT` – Backend server port (default: `5000`)  

## API Endpoints
Core Banking:
- `GET  /api/health` – Health check  
- `POST /api/transfers/intra-bank` – Transfer between own accounts  
- `POST /api/transfers/inter-bank` – External ACH/wire transfer  
- `GET  /api/transfers/:id` – Transfer status & history  

Legacy Insurance:
- `POST /api/auth/login` – User auth  
- `GET  /api/policies` – List user policies  
- `POST /api/policies/buy` – Purchase new policy  
- `GET  /api/premiums/deductions` – Deduction history  

## Features
- **Account Transfer System**  
  - Intra-bank instant transfers  
  - Scheduled inter-bank ACH transfers  
  - Idempotency keys & duplicate prevention  
- **Insurance Premium Engine**  
  - Daily UTC deductions at configured time  
  - Auto-marking of defaulters with insufficient balance  
- Cross-cutting
  - Comprehensive observability & logging  
  - Health-check endpoints for all critical services  
  - Transaction management across legacy & new modules  

## Testing
Run the entire test and build pipeline:  
`./setup_and_test.sh`
