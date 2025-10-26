from sqlalchemy.orm import Session
from models import User, Account
from sqlalchemy import text


def get_user_by_pan(db: Session, pan: str):
    return db.query(User).filter(User.pan_number == pan).first()


def create_account(db: Session, user: User, account_type: str, deposit: float):
    # Prefix for account type
    prefix = {"Savings": "SAV", "Current": "CUR", "FD": "FD"}[account_type]

    # Length of numeric part
    numeric_length = 12 - len(prefix)  

    # Get next value from PostgreSQL sequence
    result = db.execute(text("SELECT nextval('account_number_seq')"))
    next_account_num = result.scalar() 

    # Pad numeric part with zeros to fit total length
    padded_number = str(next_account_num).rjust(numeric_length, '0')

    # Combine prefix + padded number
    account_number = f"{prefix}{padded_number}"

    # Create account object
    account = Account(
        account_number=account_number,
        account_type=account_type,
        balance=deposit,
        user_id=user.id
    )

    # Save to DB
    db.add(account)
    db.commit()
    db.refresh(account)

    return account
