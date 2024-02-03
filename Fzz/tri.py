from typing import Optional

from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Country:
    id: int
    name: str
    iso_country: str
    description: str
    available: bool

    def __init__(self, id, name, iso_country, description, available):
        self.id = id
        self.name = name
        self.iso_country = iso_country
        self.description = description
        self.available = available


# we will separate the book object from the request because we need to validate it to be truthful

class MatchRequest(BaseModel):
    id: Optional[int]
    name: str = Field(min_length=3, max_length=30)
    iso_country: str = Field(min_length=2, max_length=4)
    theater: str = Field(min_length=1, max_length=100)
    available: bool

    class Config:
        schema_extra = {
            'example': {
                'name': 'CHINA',
                'iso_country': 'CHN',
                'theater': 'APJC',
                'available': 1
            }

        }


COUNTRY = [Country(1, 'CHINA', 'CHN', 'APJC', 0),
           Country(2, 'INDIA', 'IND', 'APJC', 1),
           Country(3, 'AUSTRALIA', 'AUS', 'APJC', 1)]


@app.get("/country_list")
async def get_country():
    return COUNTRY



@app.get("/country_list/{name}")
async def read_book(name:str):
    for i in COUNTRY:
        if i.name.lower() == name.lower():
            return i

"""
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.get("/books/rating/{rating}")
async def read_book_by_rating(rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(new_book)


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book
"""