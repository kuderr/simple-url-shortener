import typing
import random
import uuid

from pydantic import BaseModel, Field


class URL(BaseModel):
    id: int = Field(..., title="ID of URL")
    full_url: str = Field(..., title="Full URL")
    short_url_code: str = Field(..., title="Redirection code of URL")

class Database:
    """Fake db"""

    def __init__(self):
        self._items: typing.Dict[int, URL] = {}

    async def get_random(self) -> int:
        ids = list(self._items.keys())
        return random.choice(ids)

    async def get_all(self) -> typing.List[URL]:
        for url in self._items.values():
            yield url

    async def get(self, id: typing.Optional[int] = None, 
            full_url: typing.Optional[str] = None, 
            short_url_code: typing.Optional[str] = None) -> typing.Optional[URL]:
        
        if id:
            return self._items.get(id)

        try:
            return next(item for item in self._items.values()
                    if item.full_url == full_url or item.short_url_code == short_url_code)
        except StopIteration:
            return None

    async def add(self, url: str) -> URL:
        id = len(self._items) + 1
        code = uuid.uuid4().hex[:8]
        new_url = URL(id=id, full_url=url, short_url_code=code)
        self._items[id] = new_url

        return new_url

    async def delete(self, id: int) -> typing.Union[typing.NoReturn, None]:
        """
        typing.NoReturn means that method raises an error
        else it returns None as any other method/function with no 'return' specified

        same as typing.Optional[typing.NoReturn]
        """

        if id in self._items:
            del self._items[id]
        else:
            raise ValueError("URL doesn`t exist")


