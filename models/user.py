from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base  # or from database import Base

class User(Base):
    """User table in database"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)

    # Remove direct team link
    # team_id = Column(Integer, ForeignKey("teams.id"))   ❌
    # team = relationship("Team", back_populates="users") ❌

    # Team memberships through TeamMember
    teams = relationship("TeamMember", back_populates="user")

    # Tasks owned by this user
    tasks = relationship("Task", back_populates="owner")
