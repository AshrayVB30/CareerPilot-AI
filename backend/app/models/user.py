# models for database schema (SQLAlchemy models).
# pyrefly: ignore [missing-import]
from datetime import datetime
# import database models and base
# pyrefly: ignore [missing-import]
from sqlalchemy import Boolean, DateTime, String    
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column, relationship
# import base from database
# pyrefly: ignore [missing-import]
from app.db.database import Base

# create user model(represents users table in PostgreSQL)
class User(Base):
    __tablename__ = "users"

    # user id (primary key)
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    # user email (unique and indexed)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    # user password hash
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # user active status (default: True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    # user creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    # user updated timestamp
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # one-to-one relationship with CandidateProfile
    # uselist=False because one user has exactly one profile
    profile = relationship(
        "CandidateProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )