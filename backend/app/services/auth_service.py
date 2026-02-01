from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

# ---------------------------------
# CREATE USER (SAFE)
# ---------------------------------

def create_user(db: Session, email: str, password: str):
    """
    Creates a user only if it does not already exist.
    If user exists, returns the existing user.
    Fixes UNIQUE constraint crash.
    """

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return existing_user

    user = User(
        email=email,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------------------------
# AUTHENTICATE USER
# ---------------------------------

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# ---------------------------------
# JWT TOKEN
# ---------------------------------

def generate_token(user: User):
    return create_access_token(str(user.id))
