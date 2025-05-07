from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionCreate(BaseModel):
    receiver_wallet_id: int
    amount: float

class TransactionResponse(BaseModel):
    id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: float
    created_at: datetime

    class Config:
        orm_mode = True