from abc import ABC, abstractmethod
from uuid import UUID
from uuid import  uuid4
from typing import List, Optional, Any

import requests

from src.library_catalog.core.base_api import BaseApiClient
from src.library_catalog.models.schemas import BookWithID, BookCreate, BookUpdate

from dotenv import load_dotenv
import os

load_dotenv()


class AbstractBookRepository(ABC):
    @abstractmethod
    def get_books(self, title: Optional[str] = None, author: Optional[str] = None) -> List[BookWithID]:
        """Получить все книги с возможностью фильтрации по жанру"""
        pass

    @abstractmethod
    def get_book(self, book_id: UUID) -> Optional[BookWithID]:
        """Получить информацию о конкретной книге по ID"""
        pass

    @abstractmethod
    def create_book(self, book_create: BookCreate) -> BookWithID:
        """Добавить новую книгу"""
        pass

    @abstractmethod
    def update_book(self, book_id: UUID, book_update: BookUpdate) -> Optional[BookWithID]:
        """Обновить информацию о книге"""
        pass

    @abstractmethod
    def delete_book(self, book_id: UUID) -> bool:
        """Удалить книгу"""
        pass



class JsonBinBookRepository(BaseApiClient, AbstractBookRepository):
    BASE_URL = os.getenv("JSONBIN_API_URL")

    def __init__(self):
        self.bin_id = os.getenv("BIN_ID")
        self.api_key = os.getenv("MASTER_KEY")
        if not self.bin_id or not self.api_key:
            raise ValueError("Missing bin_id or api_key")
        self.headers = {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        try:
            response = requests.request(
                method,
                f"{self.BASE_URL}{endpoint}",
                headers=self.headers,
                **kwargs,
                timeout=5,
            )
            return self._handle_response(response)
        except requests.RequestException:
            return None

    def _handle_response(self, response: requests.Response) -> Any:
        response.raise_for_status()
        return response.json()

    def get_books(self, title: Optional[str] = None, author: Optional[str] = None) -> List[BookWithID]:
        data = self._make_request("GET", f"/b/{self.bin_id}")
        books = [BookWithID(**item) for item in data['record']]
        if title:
            books = [book for book in books if title.lower() in book.title.lower()]
        if author:
            books = [book for book in books if author.lower() in book.author.lower()]
        return books

    def get_book(self, book_id: UUID) -> Optional[BookWithID]:
        books = self.get_books()
        for book in books:
            if book.id == book_id:
                return book
        return None

    def create_book(self, book_create: BookCreate) -> BookWithID:
        books = self.get_books()
        new_book = BookWithID(id=uuid4(), **book_create.model_dump())
        books.append(new_book)

        books_data = [
            {
                "id": str(book.id),
                **book.model_dump(exclude={"id"})
            }
            for book in books
        ]

        response = self._make_request('PUT', f"/b/{self.bin_id}", json=books_data)
        return new_book

    def update_book(self, book_id: UUID, book_update: BookUpdate) -> Optional[BookWithID]:
        books = self.get_books()

        for index, book in enumerate(books):
            if book.id == book_id:
                updated_book = book.model_copy(update=book_update.model_dump(exclude_unset=True))
                books[index] = updated_book

                books_data = [
                    {
                        "id": str(book.id),
                        **book.model_dump(exclude={"id"})
                    }
                    for book in books
                ]


                response = self._make_request(
                    "PUT",
                    f"/b/{self.bin_id}",
                    json=books_data
                )

                return updated_book

    def delete_book(self, book_id: UUID) -> bool:
        books = self.get_books()
        initial_count = len(books)
        books = [book for book in books if book.id != book_id]

        if len(books) == initial_count:
            raise ValueError(f"Book with ID {book_id} not found")

        books_data = [
            {
                "id": str(book.id),
                **book.model_dump(exclude={"id"})
            }
            for book in books
        ]

        response = self._make_request(
            "PUT",
            f"/b/{self.bin_id}",
            json=books_data
        )

        return True