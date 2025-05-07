from models.user import User
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional

User.wallets = relationship("Wallet", back_populates="user")

# Pydantic Models
class WalletCreate(BaseModel):
    initial_balance: Optional[float] = 0.0

class WalletAddFunds(BaseModel):
    amount: float

class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float

    class Config:
        orm_mode = True