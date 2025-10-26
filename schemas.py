from pydantic import BaseModel, validator

class TokenRequest(BaseModel):
    pan_number: str

class AccountRequestWithPAN(BaseModel):
    pan_number: str
    account_type: str
    initial_deposit: float

class AllAccountRequest(BaseModel):
    pan_number: str    

