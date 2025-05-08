from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.tier import Tier

def initialize_tiers(db: Session):
    tiers = [
        {"name": "Basic", "max_balance": 1000.0},
        {"name": "Silver", "max_balance": 5000.0},
        {"name": "Premium Merchant", "max_balance": 50000.0},
    ]
    for tier in tiers:
        existing_tier = db.query(Tier).filter(Tier.name == tier["name"]).first()
        if not existing_tier:
            db_tier = Tier(name=tier["name"], max_balance=tier["max_balance"])
            db.add(db_tier)
    db.commit()

def get_tier_by_name(db: Session, tier_name: str):
    tier = db.query(Tier).filter(Tier.name == tier_name).first()
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tier {tier_name} not found"
        )
    return tier

def get_user_tier(db: Session, user_id: int):
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.tier