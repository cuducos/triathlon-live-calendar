from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

DEFAULT_EXPIRES_IN = timedelta(days=1)


@dataclass
class Response:
    content: str
    expires_on: datetime


@dataclass
class Cache:
    _response: Optional[Response] = None

    @property
    def response(self) -> Optional[str]:
        if not self._response:
            return None

        if self._response.expires_on < datetime.now():
            return None

        return self._response.content

    def save(self, content: str, expires_in: Optional[timedelta] = None) -> None:
        expires_in = expires_in or DEFAULT_EXPIRES_IN
        self._response = Response(content, datetime.now() + expires_in)
