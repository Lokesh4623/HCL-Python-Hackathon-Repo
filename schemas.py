from pydantic import BaseModel, validator

class AccountRequest(BaseModel):
    account_type: str
    initial_deposit: float

class TokenRequest(BaseModel):
    pan_number: str

