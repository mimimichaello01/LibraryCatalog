import requests
from typing import Any, Optional
from api.base_client import BaseApiClient


class OpenLibraryClient(BaseApiClient):
    BASE_URL = "https://openlibrary.org"

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        try:
            response = requests.request(
                method,
                f"{self.BASE_URL}{endpoint}",
                **kwargs,
                timeout=5
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            print(f"Request faild: {e}")
            return None


    def _handle_response(self, response: requests.Response) -> Optional[Any]:
        if response.status_code == 200:
            return response.json()
        return None

    def _get_first_doc_by_title(self, title: str) -> Optional[dict]:
        data = self._make_request("GET", "/search.json", params={"title": title})
        return data.get("docs", [{}])[0] if data else None

    def get_cover_id_by_title(self, title: str) -> Optional[str]:
        doc = self._get_first_doc_by_title(title)
        if not doc:
            return None
        cover_id = doc.get("cover_i")
        if not cover_id:
            return None
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    def get_description_by_title(self, title: str) -> Optional[str]:
        doc = self._get_first_doc_by_title(title)
        if not doc:
            return None
        desc = doc.get("description")
        if isinstance(desc, dict):
            return desc.get("value")
        if isinstance(desc, str):
            return desc
        return None

    def get_rating_by_title(self, title: str) -> Optional[float]:
        doc = self._get_first_doc_by_title(title)
        if not doc:
            return None
        work_key = doc.get("key")
        if not work_key:
            return None
        data = self._make_request("GET", f"{work_key}.json")
        if not data:
            return None
        return data.get("ratings_average")
