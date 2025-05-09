from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    rating: Optional[float] = None
    author: str
    genre: str
    pages: int
    availability: bool
    cover_url: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    availability: Optional[bool] = None
    cover_url: Optional[str] = None


class BookWithID(BookBase):
    id: UUID


class BookResponse(BookWithID):
    pass