from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timezone, timedelta
from app.config import settings

def create_tokens(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    access_token = jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algoritm)

    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    }
    refresh_token = jwt.encode(payload=refresh_payload, key=settings.secret_key, algorithm=settings.algoritm)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")