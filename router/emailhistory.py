from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from model import ListOfCompanies, SentMailHistory

router = APIRouter()

@router.get("/emailhistory", status_code=status.HTTP_200_OK)
def get_email_history(db: Session = Depends(get_db)):
    all_emails = db.query(SentMailHistory).all()
    return all_emails
