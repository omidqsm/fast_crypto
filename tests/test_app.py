import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from model import User
from tests.config import async_test_session_maker, pytest_app


@pytest_asyncio.fixture(scope='module')
async def create_default_users():
    user1 = User(id=1, balance=1000)
    user2 = User(id=2, balance=2000)
    user3 = User(id=3, balance=500)
    session = async_test_session_maker()
    async with session.begin():
        session.add(user1)
        session.add(user2)
        session.add(user3)


async def test_single_trade_more_than_10_dollars(create_default_users):
    async with AsyncClient(transport=ASGITransport(app=pytest_app), base_url="http://test") as client:
        trade = {
            "user_id": 1,
            "symbol": "ABAN",
            "amount": 3
        }
        response = await client.post('/orders/trade', json=trade)
        assert response.status_code == 200
        response_data = response.json()
        for u in response_data:
            if u['id'] == 1:
                assert u['balance'] == 988
            if u['id'] == 2:
                assert u['balance'] == 2000
            if u['id'] == 3:
                assert u['balance'] == 500


async def test_less_than_10_dollar_aban_trades(create_default_users):
    async with AsyncClient(transport=ASGITransport(app=pytest_app), base_url="http://test") as client:

        # first trade
        trade_1 = {
            "user_id": 1,
            "symbol": "ABAN",
            "amount": 1
        }
        response = await client.post('/orders/trade', json=trade_1)
        assert response.status_code == 200
        response_data = response.json()

        for u in response_data:
            if u['id'] == 1:
                assert u['balance'] == 988
            if u['id'] == 2:
                assert u['balance'] == 2000
            if u['id'] == 3:
                assert u['balance'] == 500

        # second trade
        trade_2 = {
            "user_id": 2,
            "symbol": "ABAN",
            "amount": 1
        }
        response = await client.post('/orders/trade', json=trade_2)
        assert response.status_code == 200
        response_data = response.json()

        for u in response_data:
            if u['id'] == 1:
                assert u['balance'] == 988
            if u['id'] == 2:
                assert u['balance'] == 2000
            if u['id'] == 3:
                assert u['balance'] == 500

        # third trade
        trade_3 = {
            "user_id": 3,
            "symbol": "ABAN",
            "amount": 2
        }
        response = await client.post('/orders/trade', json=trade_3)
        assert response.status_code == 200
        response_data = response.json()
        for u in response_data:
            if u['id'] == 1:
                assert u['balance'] == 984
            if u['id'] == 2:
                assert u['balance'] == 1996
            if u['id'] == 3:
                assert u['balance'] == 492
