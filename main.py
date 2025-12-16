from dotenv import load_dotenv
from models.base import Base
from db import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from schema.user import UserCreate, UserResponse
from schema.task import TaskCreate, TaskResponse, TaskUpdate
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.user import User
from models.task import Task
from schema.team import TeamCreate, TeamUpdate, TeamResponse
from models.team import Team 
from models.team_member import TeamMember


# load environment variables
load_dotenv()

# create database tables
Base.metadata.create_all(bind=engine)

# server
app = FastAPI(
    title="Lyte API",
    description="Lyte API",
    version="0.0.1",
)

# CORS configuration - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Welcome to the Lyte API"}


# user endpoints
@app.get("/api/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(email=user.email, hashed_password=user.password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None


@app.get("/api/users/{user_id}/tasks", response_model=list[TaskResponse])
def get_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


@app.get("/api/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        user_id=task.user_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = task.title
    db_task.description = task.description
    db_task.priority = task.priority
    db_task.status = task.status
    db_task.user_id = task.user_id
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None

@app.post("/api/teams", response_model=TeamResponse, status_code=201)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    try:
        db_team = Team(
            name=team.name,
            # description=team.description,
            # user_id=team.user_id,
        )
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@app.get("/api/teams", response_model=list[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    try:
        teams = db.query(Team).all()
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

@app.get("/api/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.put("/api/teams/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_team.name = team.name
    # db_team.description = team.description
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.delete("/api/teams/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return None


@app.post("/api/teams/{team_id}/members/assign")
def assign_user_to_team(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_team = db.query(Team).filter(Team.id== team_id).first()
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_team or not db_user:
        raise HTTPException(status_code=404, detail="Team or user not found")

    try:
        db_team.users.append(db_user)
        db.commit()
        db.refresh(db_team)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return db_team

@app.post("/api/teams/{team_id}/members")
def add_team_member(team_id: int, user_id: int, role: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not team or not user:
        raise HTTPException(status_code=404, detail="Team or user not found")

    member = TeamMember(team_id=team_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    db.refresh(member)

    return {
        "user_id": user.id,
        "team_id": team.id,
        "role": role
    }

@app.get("/api/teams/{team_id}/members")
def get_team_members(team_id: int, db: Session = Depends(get_db)):
    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    if not members:
        raise HTTPException(status_code=404, detail="No members found")

    return [
        {
            "user_id": m.user.id,
            "name": m.user.name,
            "role": m.role
        }
        for m in members
    ]


