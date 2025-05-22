from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import make_db, clean_db, fill_db
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_db()
    await fill_db()
    yield
    await clean_db()


def main():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router=router)
    uvicorn.run(app, host='0.0.0.0')


if __name__ == '__main__':
    main()
