from sqlalchemy.orm import Session
from models import User, Account
import uuid

def get_user_by_pan(db: Session, pan: str):
    return db.query(User).filter(User.pan_number == pan).first()

def create_account(db: Session, user: User, account_type: str, deposit: float):
    prefix = {"Savings": "SAV", "Current": "CUR", "FD": "FD"}[account_type]
    account_number = prefix + str(uuid.uuid4().int)[:9]
    account = Account(
        account_number=account_number,
        account_type=account_type,
        balance=deposit,
        user_id=user.id
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
