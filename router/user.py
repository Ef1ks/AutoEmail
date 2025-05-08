from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from funkcje.hashing import hash_password
from model import User
from schemat import CreateUser, ResponseCreateUser, ResponseListUsers, ResponseSingleUser

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register",  status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    existing_user = db.query(User).filter((User.email == user.email) | (User.nickname == user.nickname)).first()
    if existing_user:
        if user.nickname == existing_user.nickname:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {user.email} is already registered in database.")
        if user.email == existing_user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Nickname {user.nickname} is already registered in database."
            )
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
