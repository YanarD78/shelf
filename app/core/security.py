import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from app.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError



# Tokens
def create_tokens(user_id: int) -> dict[str, str]:
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

def _decode_token(token: str, expected_type: str) -> int:
    try:

        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]}
        )

        if payload.get("type") != expected_type:
            raise jwt.InvalidTokenError("Invalid token type")

        user_id = payload.get("sub")
        if user_id is None:
            raise jwt.InvalidTokenError("Could not validate credentials")

        return int(user_id)
        
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except (jwt.InvalidTokenError, ValueError):
        raise InvalidTokenError()

def decode_access_token(token: str) -> int:
    return _decode_token(token=token, expected_type="access")

def decode_refresh_token(token: str) -> int:
    return _decode_token(token=token, expected_type="refresh")



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