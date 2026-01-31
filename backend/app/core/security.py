import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from cryptography.fernet import Fernet

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def hash_password(password: str) -> str:
    # bcrypt max length protection
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password[:72], hashed)

# JWT
SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Encryption for Jira tokens
FERNET_KEY = os.getenv("JIRA_ENCRYPTION_KEY")

if not FERNET_KEY:
    # generate once and put in .env
    FERNET_KEY = Fernet.generate_key().decode()
    print("⚠️ Generated dev encryption key:", FERNET_KEY)

fernet = Fernet(FERNET_KEY)

def encrypt_secret(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_secret(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()
