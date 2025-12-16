from pydantic import BaseModel
from typing import List, Optional


class TeamCreate(BaseModel):
    name: str
    # description: str | None = None

class TeamUpdate(BaseModel):
    name: str | None = None
    # description: str | None = None

class TeamResponse(BaseModel):
    id: int
    name: str
    # description: str | None = None


    class Config:
        from_attributes = True
        orm_mode = True

TeamResponse.update_forward_refs()

