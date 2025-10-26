import re
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import TokenRequest, AccountRequestWithPAN, AllAccountRequest
from crud import get_user_by_pan, create_account
from auth import create_jwt, verify_token
from models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PAN-Based Account API with JWT")

MIN_DEPOSIT = {"Savings": 1000, "Current": 5000, "FD": 10000}
PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"

# -------------------
# JWT Token Endpoint
# -------------------
@app.post("/generate-token")
def generate_token(data: TokenRequest, db: Session = Depends(get_db)):
    # Validate PAN format
    if not re.match(PAN_REGEX, data.pan_number):
        raise HTTPException(status_code=400, detail="Invalid PAN format")

    user = get_user_by_pan(db, data.pan_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = create_jwt(data.pan_number)
    return {"jwt": token}

# -------------------
# Create Account Endpoint (PAN in payload)
# -------------------
@app.post("/accounts/create")
def create_account_endpoint(
    data: AccountRequestWithPAN,  # includes pan_number
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    # Validate PAN format
    if not re.match(PAN_REGEX, data.pan_number):
        raise HTTPException(status_code=400, detail="Invalid PAN format")

    # Extract token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token header")
    token = authorization[7:]

    # Verify JWT and ensure PAN matches
    token_pan = verify_token(token)
    if token_pan != data.pan_number:
        raise HTTPException(status_code=403, detail="Token does not match PAN")

    # Fetch user
    user = get_user_by_pan(db, data.pan_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate Account Type and initial deposit
    min_dep = MIN_DEPOSIT.get(data.account_type)
    if min_dep is None:
        raise HTTPException(status_code=400, detail="Invalid account type! Must be Savings, Current, or FD")
    if data.initial_deposit < min_dep:
        raise HTTPException(status_code=400, detail=f"Minimum deposit for {data.account_type} is {min_dep}")

    # Create account
    account = create_account(db, user, data.account_type, data.initial_deposit)

    return {"message": f"Your {data.account_type} account created successfully with the account number {account.account_number}"}

# -------------------
# Get Accounts Endpoint (PAN in payload)
# -------------------
@app.get("/accounts")
def get_accounts(
    data: AllAccountRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    pan_number = data.pan_number
    if not pan_number or not re.match(PAN_REGEX, pan_number):
        raise HTTPException(status_code=400, detail="Invalid PAN format")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token header")
    token = authorization[7:]

    # Verify JWT and PAN
    token_pan = verify_token(token)
    if token_pan != pan_number:
        raise HTTPException(status_code=403, detail="Token does not match PAN")

    user = get_user_by_pan(db, pan_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [{"account_number": a.account_number,
             "account_type": a.account_type,
             "balance": a.balance} for a in user.accounts]
