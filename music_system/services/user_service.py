from sqlalchemy.orm import Session
from music_system.models.user import User
from music_system.schemas.user import UserCreate
from music_system.utils.hashing_utils import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        username = user.username,
        email = str(user.email),
        password_hash = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
