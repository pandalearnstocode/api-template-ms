from fastapi import Depends, FastAPI
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware

from app.core import auth
from app.db import create_db_and_tables, get_session
from app.models import Task, TaskCreate
from app.routes import views

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(views.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.post("/task/", response_model=Task)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task