from typing import Optional
from pydantic import BaseModel


class UserTask(BaseModel):
    """Tasks assigned to a user"""
    user_id: int


class TaskCreate(BaseModel):
    """Task creation schema"""
    title: str
    description: str
    priority: int
    status: str
    user_id: int


class TaskUpdate(BaseModel):
    """Task update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    user_id: Optional[int] = None


class TaskResponse(BaseModel):
    """Task response schema"""
    id: int
    title: str
    description: str
    priority: int
    status: str
    user_id: int

    class Config:
        from_attributes = True
