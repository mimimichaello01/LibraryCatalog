from abc import ABC, abstractmethod
import requests
from typing import Optional, Any


class BaseApiClient(ABC):
    BASE_URL: str

    @abstractmethod
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    def _handle_response(self, response: requests.Response) -> Optional[Any]:
        pass
