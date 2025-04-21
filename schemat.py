from datetime import datetime
from os.path import split

import timestamp
from fastapi import HTTPException
from psycopg2.errorcodes import CLASS_LOCATOR_EXCEPTION
from pydantic import BaseModel, EmailStr, field_validator, model_validator, root_validator


class createFirma(BaseModel):
    email: EmailStr
    class Config:
        from_attributes = True

class createSinglePost(BaseModel):
    subject: str
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    user_email: EmailStr
    user_password: str
    user_name: str | None = None
    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def default_name(self):
        if self.user_name is None and self.user_email:
            self.user_name=self.user_email.split("@")[0]
        return self

class ResponseCreateUser(BaseModel):
    user_id: int
    email: EmailStr
    name: str
    created_at: datetime
    class Config:
        from_attributes = True

class ResponseListUsers(BaseModel):
    user_id: int
    name: str
    class Config:
        from_attributes = True

class ResponseSingleUser(BaseModel):
    user_id: int
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
    user_id: int
    email: EmailStr | None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token_from_user: str

class TokenData(BaseModel):
    id: int

class AddCompanyModel(BaseModel):
    company_name: str
    company_email: EmailStr
    class Config:
        from_attributes = True

class CompanyMailCollector(BaseModel):
    company_email: str
    class Config:
        from_attributes = True

class SingleMailAttributes(BaseModel):
    company_email: EmailStr | None = None
    company_name: str | None = None
    subject: str
    content: str
    class Config:
        from_attributes = True


class MultiMailAttributes(BaseModel):
    subject: str
    content: str
    class Config:
        from_attributes = True

