# Core Banking Platform

### Setup
1. `docker-compose up -d` (Postgres)
2. `cd backend && alembic upgrade head && python -c "from app.main import app; from app.models import Base, engine; Base.metadata.create_all(engine)"`
3. `cd backend && pytest`
4. `cd frontend && npm i && npm run dev`
