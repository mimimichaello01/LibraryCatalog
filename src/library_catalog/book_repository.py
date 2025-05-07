import json
from pathlib import Path
from typing import List


class BookRepository:
    BOOKS_DB_PATH = "books_db.json"

    def __init__(self, path: str = BOOKS_DB_PATH):
        self.path = Path(path)
        self.path.touch(exist_ok=True)
        if self.path.read_text().strip() == "":
            self.save_data([])

    def load_data(self) -> List[dict]:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, new_book: dict):
        books = self.load_data()
        books.append(new_book)

        with self.path.open("w", encoding="utf-8") as f:
            json.dump(books, f, indent=4, ensure_ascii=False)

    def save_all_data(self, books: List[dict]):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(books, f, indent=4, ensure_ascii=False)

