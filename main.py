from fastapi import FastAPI
from controllers import auth_controller, wallet_controller, transaction_controller, tier_controller
from db.database import engine, SessionLocal
from services.tier_service import initialize_tiers
from models import user, wallet
from db.database import Base


# Create database tables
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    initialize_tiers(db)

app = FastAPI(title="Digital Wallet API")

# Include routes
app.include_router(auth_controller.router)
app.include_router(wallet_controller.router)
app.include_router(transaction_controller.router)
app.include_router(tier_controller.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Digital Wallet API"}