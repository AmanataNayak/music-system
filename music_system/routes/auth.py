from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from music_system.services.user_service import create_user, get_user_by_username
from music_system.schemas.user import UserCreate, UserOut, LoginRequest, TokenResponse
from music_system.database import get_db
from music_system.utils.hashing_utils import verify_password
from music_system.utils.jwt_handler import create_access_token, decode_access_token
from music_system.middleware.auth_middleware import get_current_user
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exist."
        )
    return create_user(db=db, user=user)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserOut)
def get_current_user(current_user: UserOut = Depends(get_current_user)):
    return current_user