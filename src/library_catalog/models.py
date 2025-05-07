from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    rating: Optional[float] = None
    author: str
    genre: str
    pages: int
    availability: bool
    cover_url: Optional[str] = None
