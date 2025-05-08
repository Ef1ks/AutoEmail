from typing import Optional, Annotated

from starlette import status
from funkcje.wysylka import send_mail
from model import ListOfCompanies, SentMailHistory
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from schemat import SingleMailAttributes, TokenData, MultiMailAttributes, attachment_dir
from fastapi import Depends, APIRouter, HTTPException, UploadFile, File, Form
from database import get_db
router = APIRouter(prefix="/send")

@router.post("/one", status_code=status.HTTP_200_OK)
async def send_single_email(payload: str = Form(...)
                            , db: Session = Depends(get_db), get_current_user: TokenData = Depends(get_current_user)
                            ):


    # try:
    #     payload = SingleMailAttributes.model_validate_json(payload)  # Parsujemy string JSON do obiektu Pydantic
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #                         detail=f"Błąd podczas parsowania payload JSON: {e}")
    # if not payload.email and not payload.name:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not enough data has been entered")
    # company = db.query(ListOfCompanies).filter((ListOfCompanies.email == payload.email) | (ListOfCompanies.name == payload.name)).first()
    # if not company:
    #     if not payload.email:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email has not been entered")
    #     company=ListOfCompanies(
    #         email=str(payload.email),
    #         name=payload.name
    #     )
    #     if not company.name:
    #         company.name= company.email.split("@")[0]
    #     db.add(company)
    #     db.commit()
    #     db.refresh(company)
    # # if file:
    # #     contents = await file.read()
    # #     with open(rf"{attachment_dir}\{file.filename}", "wb") as f:
    # #         f.write(contents)
    #
    # #send_mail(company.email, payload.subject, payload.content)
    # sent_mail = SentMailHistory(
    #     company_id=company.id,
    #     subject=payload.subject,
    #     content=payload.content,
    #     user_id=get_current_user.id
    # )
    # db.add(sent_mail)
    # db.commit()
    # db.refresh(sent_mail)
    #return sent_mail
    return payload

@router.post("/all", status_code=status.HTTP_200_OK)
def send_email_to_all(payload: MultiMailAttributes, db: Session = Depends(get_db), get_current_user: TokenData = Depends(get_current_user)):
    list_of_comapnies = db.query(ListOfCompanies).all()
    for company in list_of_comapnies:
        company_to_add=SentMailHistory(
            company_id=company.id,
            subject=payload.subject,
            content=payload.content,
            user_id=get_current_user.id
        )
        db.add(company_to_add)
        send_mail(company.email, payload.subject, payload.content)
    db.commit()






