import asyncio
import uvicorn

from db.database import DataBase

from routers.menus import menus
from routers.submenus import submenus
from routers.dishes import dishes

from fastapi import FastAPI

db = DataBase()
app = FastAPI()
app.include_router(menus)
app.include_router(submenus)
app.include_router(dishes)


if __name__ == "__main__":
    asyncio.run(db.connection.setup())
    uvicorn.run(app)
