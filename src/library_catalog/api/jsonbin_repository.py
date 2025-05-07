from typing import Any, List, Optional
import requests
from dotenv import load_dotenv
import os

from api.base_client import BaseApiClient



load_dotenv()


class JsonBinRepository(BaseApiClient):
    BASE_URL = "https://api.jsonbin.io/v3"

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

    def _handle_response(self, response: requests.Response) -> Optional[Any]:
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()
        return None

    def load_data(self) -> List[dict]:
        data = self._make_request("GET", f"/b/{self.bin_id}")
        return data.get("record", []) if data else []

    def save_data(self, new_book: dict) -> bool:
        books = self.load_data()
        books.append(new_book)
        return self.save_all_data(books)

    def save_all_data(self, books: List[dict]) -> bool:
        response = self._make_request("PUT", f"/b/{self.bin_id}", json=books)
        return response is not None
