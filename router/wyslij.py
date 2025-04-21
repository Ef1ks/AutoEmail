from starlette import status
from funkcje.wysylka import send_mail
from model import ListOfCompanies, SentMailHistory
from sqlalchemy.orm import Session

from oauth2 import get_current_user
from schemat import SingleMailAttributes, TokenData, MultiMailAttributes
from fastapi import Depends, APIRouter, HTTPException
from database import get_db
router = APIRouter(prefix="/send")

@router.post("/one", status_code=status.HTTP_200_OK)
def send_single_email(payload: SingleMailAttributes, db: Session = Depends(get_db), get_current_user: TokenData = Depends(get_current_user)):
    if not payload.company_email and not payload.company_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not enough data has been entered")


    company = db.query(ListOfCompanies).filter((ListOfCompanies.company_email==payload.company_email) | (ListOfCompanies.company_name==payload.company_name)).first()

    if not company:
        if not payload.company_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email has not been entered")
        company=ListOfCompanies(
            company_email=str(payload.company_email),
            company_name=payload.company_name
        )
        if not company.company_name:
            company.company_name= company.company_email.split("@")[0]
        db.add(company)
        db.commit()
        db.refresh(company)



    #send_mail(company.company_email, payload.subject, payload.content)
    sent_mail = SentMailHistory(
        company_id=company.company_id,
        subject=payload.subject,
        content=payload.content,
        user_id=get_current_user.id
    )
    db.add(sent_mail)
    db.commit()
    db.refresh(sent_mail)
    return sent_mail

@router.post("/all", status_code=status.HTTP_200_OK)
def send_email_to_all(payload: MultiMailAttributes, db: Session = Depends(get_db), get_current_user: TokenData = Depends(get_current_user)):
    list_of_comapnies = db.query(ListOfCompanies).all()
    for company in list_of_comapnies:
        company_to_add=SentMailHistory(
            company_id=company.company_id,
            subject=payload.subject,
            content=payload.content,
            user_id=get_current_user.id
        )
        db.add(company_to_add)
        send_mail(company.company_email, payload.subject, payload.content)
    db.commit()






