from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

DATABASE_URL = "sqlite:///./tasks.db"
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/tasks/")
async def read_tasks():
    query = Task.__table__.select()
    return await database.fetch_all(query)

@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    query = Task.__table__.select().where(Task.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/")
async def create_task(request: Request):
    form = await request.form()
    title = form["title"]
    description = form["description"]
    completed = False
    query = Task.__table__.insert().values(
        title=title,
        description=description,
        completed=completed
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "title": title, "description": description, "completed": completed}

@app.post("/tasks/{task_id}/update")
async def update_task_status(task_id: int, request: Request):
    form = await request.form()
    completed = "completed" in form
    query = Task.__table__.update().where(Task.id == task_id).values(
        completed=completed
    )
    await database.execute(query)
    return {"message": "Task status updated successfully"}

@app.post("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    query = Task.__table__.delete().where(Task.id == task_id)
    await database.execute(query)
    return {"message": "Task deleted successfully"}

@app.get("/")
async def home(request: Request):
    query = Task.__table__.select()
    tasks = await database.fetch_all(query)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/")
async def add_task_from_form(request: Request):
    form = await request.form()
    title = form["title"]
    description = form["description"]
    completed = False
    query = Task.__table__.insert().values(
        title=title,
        description=description,
        completed=completed
    )
    await database.execute(query)
    query = Task.__table__.select()
    tasks = await database.fetch_all(query)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})