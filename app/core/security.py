from fastapi.security import HTTPBearer
import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from app.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError



# Tokens
def create_tokens(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    access_token = jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    }
    refresh_token = jwt.encode(
        payload=refresh_payload,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def decode_token(token: str):
    try:

        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm]
        )

        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Invalid token type")

        user_id = payload.get("sub")
        if user_id is None:
            raise jwt.InvalidTokenError("Could not validate credentials")
        
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    
    return int(user_id)

oauth_scheme = HTTPBearer(auto_error=False)



# Passwords
def hash_password(password: str) -> str:
    bytes_password = password.encode("utf-8")

    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(
        password=bytes_password,
        salt=salt
    )

    return hashed_password.decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    user_password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    result = bcrypt.checkpw(
        password=user_password_bytes,
        hashed_password=hashed_password_bytes
    )
    
    return result