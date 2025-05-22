from sqlmodel import SQLModel


class TradeIn(SQLModel):
    user_id: int
    symbol: str
    amount: int
