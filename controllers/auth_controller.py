from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from resources.user import UserCreate, UserLogin, UserResponse
from services.auth_service import create_user, authenticate_user
from db.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user)
    return db_user