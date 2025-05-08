import os
from datetime import datetime
from os.path import split

import timestamp
from fastapi import HTTPException
from psycopg2.errorcodes import CLASS_LOCATOR_EXCEPTION
from pydantic import BaseModel, EmailStr, field_validator, model_validator, root_validator

from funkcje.folder import create_dir

base_dir = os.path.dirname(__file__)
attachment_dir = create_dir(base_dir)

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None
    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def default_name(self):
        if self.nickname is None and self.email:
            self.nickname=self.email.split("@")[0]
        return self

class ResponseCreateUser(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    created_at: datetime
    class Config:
        from_attributes = True

class ResponseListUsers(BaseModel):
    id: int
    nickname: str
    class Config:
        from_attributes = True

class ResponseSingleUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLoginCheck(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: str

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_email_or_name(self):
        if self.email is None and self.name is None:
            raise HTTPException(status_code=422, detail="Email or Name required")
        if self.email and self.name :
            raise HTTPException(status_code=422, detail="Only one value allowed")
        return self

class ResponseUserLogin(BaseModel):
    id: int
    email: EmailStr | None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token_from_user: str

class TokenData(BaseModel):
    id: int

class AddCompanyModel(BaseModel):
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class SingleMailAttributes(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    subject: str
    content: str
    class Config:
        from_attributes = True


class MultiMailAttributes(BaseModel):
    subject: str
    content: str
    class Config:
        from_attributes = True

