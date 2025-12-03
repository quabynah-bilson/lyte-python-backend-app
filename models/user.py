from .base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    """User table in database"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")
    teams = relationship("Team", back_populates="users")
