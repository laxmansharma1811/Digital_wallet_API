from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from resources.tier import TierResponse
from services.tier_service import get_user_tier
from db.database import get_db
from models.user import User
from fastapi import HTTPException, status

router = APIRouter(prefix="/tier", tags=["Tier"])

# Reuse authentication dependency
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@router.get("/", response_model=TierResponse)
def get_user_tier_details(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_tier(db, user.id)