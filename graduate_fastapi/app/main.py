from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books/", response_class=HTMLResponse)
def read_books(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return templates.TemplateResponse("books_list.html", {"request": request, "books": books})

@app.get("/books/{book_id}", response_class=HTMLResponse)
def read_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})

@app.get("/books/add", response_class=HTMLResponse)
def add_book_form(request: Request):
    return templates.TemplateResponse("book_add.html", {"request": request})

@app.post("/books/", response_class=HTMLResponse)
def create_book(request: Request, title: str = Form(...), author: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    book = schemas.BookCreate(title=title, author=author, description=description)
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": db_book})