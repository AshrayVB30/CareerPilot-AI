from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# DATABASE_URL - configures the database connection string.
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)
# engine - represents our database connection infrastructure.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
# SessionLocal - creates database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base - will become the foundation for our DB models
class Base(DeclarativeBase):
    pass

# get_db() - opens a DB session and ensures it closes properly after use.
# It yields the session and closes it in the finally block.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()