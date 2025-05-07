from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy Model
class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    user = relationship("User", back_populates="wallets")