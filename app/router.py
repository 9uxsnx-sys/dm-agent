from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from app.schemas import IncomingMessage, OutgoingResponse
from logic import handle_message

router = APIRouter()

@router.post("/webhook", response_model=OutgoingResponse)
async def webhook(
    payload: IncomingMessage,
    db: AsyncSession = Depends(get_db)
):
    reply = await handle_message(
        user_id=payload.user,
        message=payload.message,
        platform=payload.platform,
        db=db
    )
    return OutgoingResponse(reply=reply)
