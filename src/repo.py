from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, contains_eager

from database import get_async_session
from model import Trade, User


class TradeRepo:

    def __init__(self, session:  AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add(self, trade: Trade):
        self.session.add(trade)
        await self.session.flush()

    async def get_unsettled_trades(self, symbol: str):
        """get unlocked unsettled trades"""
        stmt = (
            select(Trade).
            options(joinedload(Trade.user, innerjoin=True)).
            where(
                Trade.symbol == symbol,
                Trade.settled == False
            ).
            with_for_update(skip_locked=True)  # skip locked rows
        )
        trades = (await self.session.scalars(stmt)).all()
        return trades


class UserRepo:
    def __init__(self, session:  AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get(self, pk: int):
        stmt = select(User).where(User.id == pk).with_for_update()
        user = await self.session.scalar(stmt)
        return user

    async def get_all(self):
        stmt = select(User).order_by(User.id)
        result = await self.session.scalars(stmt)
        return result.all()
