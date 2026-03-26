import hashlib
import json
import os
import urllib.parse
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.admin_user import AdminUser


ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 12
security = HTTPBearer(auto_error=False)


def _jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY", "")
    if not secret:
        raise HTTPException(status_code=500, detail="JWT_SECRET_KEY орнатылмаған")
    return secret


def hash_password(raw_password: str) -> str:
    pepper = os.getenv("JWT_SECRET_KEY", "math-pisa-bot-default-pepper")
    return hashlib.sha256(f"{raw_password}:{pepper}".encode("utf-8")).hexdigest()


def verify_password(raw_password: str, password_hash: str) -> bool:
    return hash_password(raw_password) == password_hash


def create_access_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, _jwt_secret(), algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен мерзімі аяқталған")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Жарамсыз токен")


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> AdminUser:
    if not credentials:
        raise HTTPException(status_code=401, detail="Авторизация қажет")

    payload = decode_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Токенде қолданушы жоқ")

    admin = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not admin or not admin.is_active:
        raise HTTPException(status_code=403, detail="Әкімші қолжетімсіз")

    return admin


def _extract_telegram_id(request: Request) -> int:
    init_data = request.headers.get("x-telegram-init-data", "")
    if not init_data or "user" not in init_data:
        raise HTTPException(status_code=401, detail="Telegram деректері жоқ")
    try:
        params = dict(urllib.parse.parse_qsl(init_data))
        user_data = json.loads(params.get("user", "{}"))
        tid = user_data.get("id")
        if not tid:
            raise ValueError
        return int(tid)
    except Exception:
        raise HTTPException(status_code=401, detail="Telegram деректері жарамсыз")


def get_admin_by_telegram_id(request: Request) -> int:
    tid = _extract_telegram_id(request)
    allowed = os.getenv("ADMIN_TELEGRAM_IDS", "")
    allowed_ids = {int(x.strip()) for x in allowed.split(",") if x.strip()}
    if tid not in allowed_ids:
        raise HTTPException(status_code=403, detail="Әкімші құқығы жоқ")
    return tid
