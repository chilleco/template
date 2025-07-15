from datetime import datetime, timedelta
import jwt
from app.core.settings import get_settings

settings = get_settings()

def create_access_token(
    data: dict, 
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, 
        settings.jwt_secret, 
        algorithm="HS256"
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
