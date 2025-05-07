from fastapi import FastAPI
from controllers import auth_controller, wallet_controller, transaction_controller
from db.database import engine
from models import user, wallet
from db.database import Base


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Wallet API")

# Include routes
app.include_router(auth_controller.router)
app.include_router(wallet_controller.router)
app.include_router(transaction_controller.router)