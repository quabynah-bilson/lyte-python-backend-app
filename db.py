# import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database setup
# DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine("postgresql://postgres:postgres@localhost:5432/lyte_inspired_db")

# session local (for database transactions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        raise
    finally:
        db.close()
