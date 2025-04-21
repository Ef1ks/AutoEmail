
from starlette import status
from model import ListOfCompanies
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from database import get_db
from schemat import AddCompanyModel, TokenData
from oauth2 import get_current_user
router = APIRouter(prefix="/add", tags=["add"])

@router.post("/company", status_code=201)
def add_company(company: AddCompanyModel, db: Session = Depends(get_db), get_current_user: TokenData = Depends(get_current_user)):
    if not db.query(ListOfCompanies).filter(ListOfCompanies.company_email == company.company_email).first() or db.query(ListOfCompanies).filter(ListOfCompanies.company_name == company.company_name).first():
        new_company=ListOfCompanies(**company.model_dump())
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        return {"detail": f"Company added to list successfully by {get_current_user.id}"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
