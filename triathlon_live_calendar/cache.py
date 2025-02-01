from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

DEFAULT_EXPIRES_IN = timedelta(days=1)


@dataclass
class Value:
    content: str
    expires_on: datetime


@dataclass
class Cache:
    _value: Optional[Value] = None

    @property
    def is_expired(self) -> bool:
        if not self._value:
            return True
        return self._value.expires_on < datetime.now()

    @property
    def value(self) -> Optional[str]:
        if self._value is None or self.is_expired:
            return None
        return self._value.content

    def save(self, content: str, expires_in: Optional[timedelta] = None) -> None:
        expires_in = expires_in or DEFAULT_EXPIRES_IN
        self._value = Value(content, datetime.now() + expires_in)
