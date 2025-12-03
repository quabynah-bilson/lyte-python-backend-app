from pydantic import BaseModel

class TeamCreate(BaseModel):
    name: str
    description: str | None = None
    user_id: int

class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class TeamResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    user_id: int

    class Config:
        orm_mode = True