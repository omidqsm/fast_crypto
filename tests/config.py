import asyncio

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from database import get_async_session
from api import router

DATABASE_URL = "sqlite+aiosqlite://"

test_engine = create_async_engine(DATABASE_URL, echo=True)
async_test_session_maker = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_test_session():
    async with async_test_session_maker() as session:
        yield session


async def init():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


asyncio.run(init())
pytest_app = FastAPI()
pytest_app.include_router(router=router)

pytest_app.dependency_overrides[get_async_session] = get_async_test_session