from pydantic import BaseModel, validator

class AccountRequest(BaseModel):
    account_type: str
    initial_deposit: float

    @validator("account_type")
    def validate_account_type(cls, v):
        if v not in ["Savings", "Current", "FD"]:
            raise ValueError("Account type must be Savings, Current, or FD")
        return v

class TokenRequest(BaseModel):
    pan_number: str

