from fastapi import APIRouter

from models import Book
from api.jsonbin_repository import JsonBinRepository
from api.external_api import OpenLibraryClient

router = APIRouter(prefix="/books", tags=["books"])

#repo = BookRepository()
repo = JsonBinRepository()
client = OpenLibraryClient()


@router.get("/")
def get_books(title: str = None, author: str = None):
    books = repo.load_data()

    if title:
        books = [book for book in books if title.lower() in book["title"].lower()]
    if author:
        books = [book for book in books if author.lower() in book["author"].lower()]

    if not books:
        return {"message": "Нет данных для отображения."}

    return books


@router.get("/{book_id}")
def get_book(book_id: int):
    books = repo.load_data()
    return next((book for book in books if book["id"] == book_id), None)


@router.post("/")
def add_book(book: Book):
    book_dict = book.model_dump()

    if cover_url := client.get_cover_id_by_title(book.title):
        book_dict["cover_url"] = cover_url

    if description := client.get_description_by_title(book.title):
        book_dict["description"] = description

    if rating := client.get_rating_by_title(book.title):
        book_dict["rating"] = rating

    repo.save_data(book_dict)
    return book_dict


@router.put("/{book_id}")
def update_book(book_id: int, updated_data: Book):
    books = repo.load_data()
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index].update(updated_data.model_dump())
            repo.save_all_data(books)
            return books[index]
    return None


@router.delete("/{book_id}")
def delete_book(book_id: int):
    books = repo.load_data()
    for index, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(index)

            repo.save_all_data(books)
            return {"message": "Книга удалена", "book": deleted_book}
    return None
