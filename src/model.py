from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    balance: float = Field(default=0)
    trades: list["Trade"] = Relationship(back_populates="user")


class Trade(SQLModel, table=True):
    __tablename__ = "trades"

    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    amount: float
    price: float
    cost: float
    settled: bool = Field(default=False, index=True)
    user_id: int = Field(foreign_key="users.id")
    user: User | None = Relationship(back_populates="trades")
