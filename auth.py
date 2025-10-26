import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "HACKATHON"

def create_jwt(pan_number: str) -> str:
    payload = {
        "pan_number": pan_number,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "token_id": str(datetime.utcnow().timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("pan_number")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
