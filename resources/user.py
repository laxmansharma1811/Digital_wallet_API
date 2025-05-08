from pydantic import BaseModel, EmailStr
from resources.tier import TierResponse


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    tier_name: str = "Basic"  # Default to Basic tier

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    tier: "TierResponse"

    class Config:
        orm_mode = True
