from sqlalchemy import Column, Integer, String, Float
from db.database import Base


# SQLAlchemy Model
class Tier(Base):
    __tablename__ = "tiers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    max_balance = Column(Float, nullable=False)