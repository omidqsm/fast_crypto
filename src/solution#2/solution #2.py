from collections import defaultdict

from fastapi import APIRouter

from settings import CRYPTO_PRICES, MIN_EXCHANGE_VAL
from schema import TradeIn
from service.external import buy_from_exchange


router = APIRouter(prefix='/orders', tags=['Order'])

user_balances = {
    1: 1000,
    2: 2000,
}


class SymbolBuffer:
    trades: list[TradeIn] | None = []
    total: int | None = 0


class TradeManager:
    def __init__(self):
        self.buffers = defaultdict(SymbolBuffer)  # a dictionary of buffers

    def add_trade_to_buffer(self, data: TradeIn):
        buffer = self.buffers[data.symbol]
        buffer.total += CRYPTO_PRICES.get(data.symbol, 0) * data.amount
        buffer.trades.append(data)
        if buffer.total >= MIN_EXCHANGE_VAL:
            self.exchange_buffer(buffer)

    @staticmethod
    def exchange_buffer(buffer: SymbolBuffer):
        symbol = buffer.trades[0].symbol
        # in transaction
        while buffer.trades:
            trade = buffer.trades.pop()
            user_balances[trade.user_id] -= CRYPTO_PRICES.get(symbol, 0) * trade.amount
        total = buffer.total
        buffer.total = 0
        buy_from_exchange(symbol, total)


trade_manager = TradeManager()


@router.post("/trade", status_code=204)
async def trade_api(
    data: TradeIn,
):
    return trade_manager.add_trade_to_buffer(data)
