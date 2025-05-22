from fastapi import APIRouter, Depends, status

from schema import TradeIn
from service.internal import TradeService

router = APIRouter()


@router.post("/trade", status_code=status.HTTP_200_OK)
async def trade_api(
    data: TradeIn,
    trade_service: TradeService = Depends(TradeService),
):
    return await trade_service.submit_trade(data)
