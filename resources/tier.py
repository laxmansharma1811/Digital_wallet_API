from pydantic import BaseModel


class TierResponse(BaseModel):
    id: int
    name: str
    max_balance: float

    class Config:
        orm_mode = True