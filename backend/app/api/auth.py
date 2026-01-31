from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth_schema import SignupRequest, LoginRequest, AuthResponse
from app.services.auth_service import create_user, authenticate_user, generate_token
from app.core.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password)
    token = generate_token(user)
    return AuthResponse(access_token=token)

@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token(user)
    return AuthResponse(access_token=token)
@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email
    }
