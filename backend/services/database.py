import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.models.policy import Base, Policy

def get_database_url():
    return os.getenv('DATABASE_URL', 'sqlite:///insurance.db')

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
    # Add seed insurance products if table is empty
    with SessionLocal() as session:
        try:
            result = session.execute(text("SELECT COUNT(*) FROM policies")).scalar()
            if result == 0:
                # Health Insurance
                health_policy = Policy(
                    user_id='SYSTEM',
                    policy_number='HEALTH-001',
                    product_code='HEALTH_BASIC',
                    premium=150.00,
                    coverage_amount=50000.00,
                    deductible=500.00,
                    start_date='2024-01-01',
                    end_date='2025-01-01',
                    status='SEED'
                )
                # Auto Insurance
                auto_policy = Policy(
                    user_id='SYSTEM',
                    policy_number='AUTO-001',
                    product_code='AUTO_COMPREHENSIVE',
                    premium=89.00,
                    coverage_amount=25000.00,
                    deductible=1000.00,
                    start_date='2024-01-01',
                    end_date='2025-01-01',
                    status='SEED'
                )
                session.add(health_policy)
                session.add(auto_policy)
                session.commit()
        except Exception as e:
            print(f"Seed error: {e}")
            session.rollback()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
