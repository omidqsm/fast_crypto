from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from model import User

DATABASE_URL = "postgresql+asyncpg://user:password@pgdb:5432/fast_ctypto_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def make_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def clean_db():
    await engine.dispose()


async def fill_db():
    user1 = User(id=1, balance=1000)
    user2 = User(id=2, balance=2000)
    user3 = User(id=3, balance=500)

    session = async_session_maker()
    try:
        async with session.begin():
            session.add(user1)
            session.add(user2)
            session.add(user3)
    except Exception as e:
        print(e)