from datetime import date

from fastapi import Depends, FastAPI
from database import get_db, engine, Base
from sqlalchemy.orm import Session
import model 
from pydantic import BaseModel

# // in this file we are createing api 
app = FastAPI()


# store data in db 

class Bookstore(BaseModel):
    id: int
    title: str
    author : str
    description: str    
    published_date: date | None = None

@app.post("/books/")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    db_book = model.Book(
        id=book.id,
        title=book.title,
        author=book.author,
        description=book.description,
        published_date=book.published_date
    )
    # add to databse 
    db.add(db_book)

    db.commit()

    db.refresh(db_book)
    
    return db_book



@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books


