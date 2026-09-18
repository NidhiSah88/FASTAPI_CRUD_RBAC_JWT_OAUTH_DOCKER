from fastapi import FastAPI
from pydantic import BaseModel 
from fastapi.exceptions import HTTPException

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},

]

app = FastAPI()

@app.get("/book")
def getbook():
    return books



@app.get("/book/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


class Book(BaseModel):
    id: int
    title: str
    author: str


@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return book


class BookUpdate(BaseModel):
    title: str
    author: str


@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: BookUpdate):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index]["title"] = updated_book.title
            books[index]["author"] = updated_book.author
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")



@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(index)
            return {"message": "Book deleted successfully", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")