import typing

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from db import URL, Database


app = FastAPI(title="URL shortener")
db = Database()


@app.get(
        "/",
        response_description="Randon URL",
        description="Get random URL from database",
        response_model=URL,
)
async def get_random():
    try:
        random_id = await db.get_random()
        url = await db.get(random_id)
    except IndexError:
        raise HTTPException(404, "URL list is empty")

    return url


@app.get("/urls",
        response_description="All urls", 
        response_model=typing.List[URL],
)
async def get_all():
    response = []
    
    async for url in db.get_all():
        response.append(url.dict())

    return response


@app.get("/{code}")
async def redirect(code: str):
    redirect_to = await db.get(short_url_code=code)
    if not redirect_to:
        raise HTTPException(404, "No url found")

    return RedirectResponse(redirect_to.full_url)


@app.post(
        "/urls/",
        response_description="Added url",
        response_model=URL,
        status_code=201,
)
async def add(url: str):
    new_url = await db.add(url)
    return new_url


@app.delete(
        "/urls/{id}",
        response_description="Deleted URL"
)
async def delete(id: int):
    try:
        await db.delete(id)
    except ValueError as e:
        raise HTTPException(404, str(e))

    return {"msg": "URL deleted"}
