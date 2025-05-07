from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from resources.transactions import TransactionCreate, TransactionResponse
from services.transaction_service import create_transaction, get_transaction_history
from db.database import get_db
from models.user import User
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Reuse dependency to check if user exists
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_user_transaction(
    transaction: TransactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_transaction(db, user.id, transaction)

@router.get("/", response_model=List[TransactionResponse])
def get_user_transaction_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_transaction_history(db, user.id)