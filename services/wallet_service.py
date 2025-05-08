from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.wallet import Wallet
from resources.wallet import WalletCreate, WalletAddFunds
from models.user import User
from services.tier_service import get_user_tier

def create_wallet(db: Session, user_id: int, wallet: WalletCreate):
    # Check if user already has a wallet
    existing_wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if existing_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a wallet"
        )
    
    # Get user's tier
    tier = get_user_tier(db, user_id)
    
    # Validate initial balance
    if wallet.initial_balance < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Initial balance cannot be negative"
        )
    if wallet.initial_balance > tier.max_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Initial balance exceeds {tier.name} tier limit of {tier.max_balance}"
        )
    
    # Create new wallet
    db_wallet = Wallet(user_id=user_id, balance=wallet.initial_balance)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def get_wallet(db: Session, user_id: int):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return wallet

def add_funds(db: Session, user_id: int, funds: WalletAddFunds):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    if funds.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )
    
    # Get user's tier
    tier = get_user_tier(db, user_id)
    
    # Check if new balance exceeds tier limit
    new_balance = wallet.balance + funds.amount
    if new_balance > tier.max_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"New balance would exceed {tier.name} tier limit of {tier.max_balance}"
        )
    
    wallet.balance = new_balance
    db.commit()
    db.refresh(wallet)
    return wallet