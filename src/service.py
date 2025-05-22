from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from settings import CRYPTO_PRICES, MIN_EXCHANGE_VAL
from database import get_async_session
from model import Trade
from repo import TradeRepo, UserRepo
from schema import TradeIn


class TradeService:
    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session),
            trade_repo: TradeRepo = Depends(TradeRepo),
            user_repo: UserRepo = Depends(UserRepo),
    ):
        self.session = session
        self.trade_repo = trade_repo
        self.user_repo = user_repo

    async def buy_from_exchange(self, symbol: str, cost: int):
        print(f'exchange was done for symbol {symbol} for cost {cost}$')

    async def submit_trade(self, data: TradeIn):
        async with self.session.begin():
            symbol = data.symbol

            price = CRYPTO_PRICES.get(symbol)

            if not price:
                raise HTTPException(status_code=400, detail="Invalid symbol")

            cost = price * data.amount

            user = await self.user_repo.get(data.user_id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if user.balance < cost:
                raise HTTPException(status_code=400, detail="Insufficient balance")

            new_trade = Trade(
                user_id=data.user_id,
                symbol=symbol,
                amount=data.amount,
                price=price,
                cost=cost,
                settled=True
            )
            if cost >= MIN_EXCHANGE_VAL:
                await self.trade_repo.add(new_trade)
                user.balance -= cost
                await self.buy_from_exchange(symbol, cost)
            else:
                new_trade.settled = False
                await self.trade_repo.add(new_trade)

                # read pending trades
                trades = await self.trade_repo.get_unsettled_trades(symbol)
                total_cost = sum(t.cost for t in trades)

                if total_cost >= MIN_EXCHANGE_VAL:
                    for t in trades:
                        t.user.balance -= t.cost
                        t.settled = 1
                    await self.session.flush()
                    await self.buy_from_exchange(symbol, total_cost)

        return await self.user_repo.get_all()
