import email

from fastapi import APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from funkcje.hashing import hash_password, check_password
from model import User
from oauth2 import create_access_token

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
def login_request(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), ):
    dane=db.query(User).filter((User.email == user_data.username) | (User.nickname == user_data.username)).first()
    if not dane:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Podany użytkownik nie istnieje")
    if not check_password(password=user_data.password, hashed_password=dane.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Błędne hasło")


    access_token_of_user = create_access_token(data={ "user_id": dane.id})


    return {"access_token": access_token_of_user}
