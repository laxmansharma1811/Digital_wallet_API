from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from resources.transactions import TransactionCreate
from models.transactions import Transaction
from models.wallet import Wallet
from models.user import User

def create_transaction(db: Session, user_id: int, transaction: TransactionCreate):
    # Get sender's wallet
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not sender_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sender wallet not found"
        )

    # Get receiver's wallet
    receiver_wallet = db.query(Wallet).filter(Wallet.id == transaction.receiver_wallet_id).first()
    if not receiver_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver wallet not found"
        )

    # Validate transaction
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )
    if sender_wallet.balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    if sender_wallet.id == receiver_wallet.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to the same wallet"
        )

    # Update balances
    sender_wallet.balance -= transaction.amount
    receiver_wallet.balance += transaction.amount

    # Create transaction record
    db_transaction = Transaction(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=transaction.amount
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction



def get_transaction_history(db: Session, user_id: int):
    # Get user's wallet
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

    # Get transactions where the user is sender or receiver
    transactions = db.query(Transaction).filter(
        (Transaction.sender_wallet_id == wallet.id) | (Transaction.receiver_wallet_id == wallet.id)
    ).all()
    return transactions