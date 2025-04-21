from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from settings import settings
from starlette import status
from schemat import TokenData

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = int((datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    data_to_encode.update({"exp": expire})

    token = jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_access_token(token_from_user: str, credentials_exception):
    try:
        data_from_token = jwt.decode(token_from_user, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = data_from_token.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)