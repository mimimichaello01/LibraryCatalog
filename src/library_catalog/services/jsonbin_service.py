from abc import ABC, abstractmethod
from typing import List, Optional
from src.library_catalog.models.schemas import BookWithID, BookCreate, BookUpdate
from uuid import UUID

from src.library_catalog.repositories.jsonbin_repo import JsonBinBookRepository
from src.library_catalog.services.open_library_service import OpenLibraryService


class JsonBinService(ABC):
    @abstractmethod
    def get_books(self, title: Optional[str] = None, author: Optional[str] = None) -> List[BookWithID]:
        pass

    @abstractmethod
    def get_book(self, book_id: UUID) -> Optional[BookWithID]:
        pass

    @abstractmethod
    def create_book(self, book_create: BookCreate) -> BookWithID:
        pass

    @abstractmethod
    def update_book(self, book_id: UUID, book_update: BookUpdate) -> Optional[BookWithID]:
        pass

    @abstractmethod
    def delete_book(self, book_id: UUID):
        pass


class JsonBinServiceImpl(JsonBinService):
    def __init__(self, repo: JsonBinBookRepository, openlib: OpenLibraryService):
        self.repo = repo
        self.openlib = openlib

    def get_books(self, title: Optional[str] = None, author: Optional[str] = None):
        return self.repo.get_books(title, author)

    def get_book(self, book_id: UUID) -> BookWithID:
        if book := self.repo.get_book(book_id):
            return book
        raise ValueError(f"Книги с ID {book_id} не существует")

    def create_book(self, book_create: BookCreate) -> BookWithID:
        if not book_create.cover_url:
            book_create.cover_url = self.openlib.get_cover_id_by_title(book_create.title)

        if not book_create.description:
            book_create.description = self.openlib.get_description_by_title(book_create.title)

        if book_create.rating is None:
            book_create.rating = self.openlib.get_rating_by_title(book_create.title)

        return self.repo.create_book(book_create)

    def update_book(self, book_id: UUID, book_update: BookUpdate) -> BookWithID:
        if updated := self.repo.update_book(book_id, book_update):
            return updated
        raise ValueError(f"Книга с ID {book_id} не найдена")

    def delete_book(self, book_id: UUID):
        deleted = self.repo.delete_book(book_id)
        if not deleted:
            raise ValueError(f"Книга с ID {book_id} не найдена")
