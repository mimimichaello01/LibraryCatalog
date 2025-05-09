from fastapi import APIRouter, Depends, Response, status
from uuid import UUID

from .dependencies import get_jsonbin_service
from src.library_catalog.models.schemas import BookWithID, BookCreate, BookUpdate
from src.library_catalog.services.jsonbin_service import JsonBinService

book_router = APIRouter(prefix="/books", tags=["books"])

@book_router.get("/", response_model=list[BookWithID])
def get_books(title: str = None,
              author: str = None,
              service: JsonBinService = Depends(get_jsonbin_service)):
    return service.get_books(title, author)

@book_router.get("/{book_id}", response_model=BookWithID)
def get_book(book_id: UUID,
             service: JsonBinService = Depends(get_jsonbin_service)):
    return service.get_book(book_id)

@book_router.post("/", response_model=BookWithID)
def create_book(book_create: BookCreate,
                service: JsonBinService = Depends(get_jsonbin_service)):
    return service.create_book(book_create)

@book_router.put("/{book_id}", response_model=BookWithID)
def update_book(book_id: UUID,
                updated_book: BookUpdate,
                service: JsonBinService = Depends(get_jsonbin_service)):
    return service.update_book(book_id, updated_book)

@book_router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: UUID,
    service: JsonBinService = Depends(get_jsonbin_service)
):
    service.delete_book(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)