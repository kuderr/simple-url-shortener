import typing
import random
import uuid

from pydantic import BaseModel, Field


class URL(BaseModel):
    """
    FastAPI uses pydantic to validate and represent data.
    Maybe dive deeper in it.
    """
    
    id: int = Field(..., title="ID of URL")
    full_url: str = Field(..., title="Full URL")
    short_url_code: str = Field(..., title="Redirection code of URL")

class Database:
    """
    Fake db
    When using with real -- all CRUD should be awaited
    """

    def __init__(self):
        self._items: typing.Dict[int, URL] = {}

    async def get_random(self) -> int:
        """
        Create list from dict_keys, because it is not supported in random.choice
        """
        ids = list(self._items.keys())
        return random.choice(ids)

    async def get_all(self) -> typing.List[URL]:
        """
        To work with large collections of data better use generators, to give an item one at a time.
        Combo with asyncio allows async for loop. With real db you will be awaiting reads from it.
        """
        for url in self._items.values():
            yield url

    async def get(self, id: typing.Optional[int] = None, 
            full_url: typing.Optional[str] = None, 
            short_url_code: typing.Optional[str] = None) -> typing.Optional[URL]:
        """
        Simulate get from db like in sqlalchemy, where u can .get by 'key'
        """
        if id:
            return self._items.get(id)

        try:
            return next(item for item in self._items.values()
                    if item.full_url == full_url or item.short_url_code == short_url_code)
        except StopIteration:
            return None

    async def add(self, url: str) -> URL:
        """
        DB create simulation. 
        Better check 'code' in db for duplicate, but not here, cause it`s an example project.
        """
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


