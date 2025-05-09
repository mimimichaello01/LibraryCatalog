from abc import ABC, abstractmethod

from typing import Optional, Any

from src.library_catalog.repositories.open_library_repo import OpenLibraryRepository


class OpenLibraryService(ABC):
    @abstractmethod
    def get_cover_id_by_title(self, title: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_description_by_title(self, title: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_rating_by_title(self, title: str) -> Optional[float]:
        pass


class OpenLibraryServiceImpl(OpenLibraryService):
    def __init__(self, repo: OpenLibraryRepository):
        self.repo = repo

    def get_cover_id_by_title(self, title: str) -> Optional[str]:
        return self.repo.get_cover_id_by_title(title)

    def get_description_by_title(self, title: str) -> Optional[str]:
        return self.repo.get_description_by_title(title)

    def get_rating_by_title(self, title: str) -> Optional[float]:
        return self.repo.get_rating_by_title(title)

