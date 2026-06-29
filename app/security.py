from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt-safe trimming (industry standard)
    return pwd.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd.verify(plain_password[:72], hashed_password)

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
