from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from resources.wallet import WalletCreate, WalletAddFunds, WalletResponse
from services.wallet_service import create_wallet, get_wallet, add_funds
from db.database import get_db
from models.user import User

router = APIRouter(prefix="/wallet", tags=["Wallet"])

# Simple dependency to check if user exists (simulating authentication)
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@router.post("/", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
def create_user_wallet(
    wallet: WalletCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_wallet(db, user.id, wallet)

@router.get("/", response_model=WalletResponse)
def get_user_wallet(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_wallet(db, user.id)

@router.post("/add-funds", response_model=WalletResponse)
def add_wallet_funds(
    funds: WalletAddFunds,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_funds(db, user.id, funds)