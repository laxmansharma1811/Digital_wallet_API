from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tier_id = Column(Integer, ForeignKey("tiers.id"), nullable=False)
    tier = relationship("Tier")
    wallets = relationship("Wallet", back_populates="user")