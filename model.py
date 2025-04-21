
from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, func, ForeignKey
from database import Base
from sqlalchemy.orm import validates, relationship

class SentMailHistory(Base):
    __tablename__ = 'history_of_sent_mail'
    mail_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('list_of_companies.company_id'))
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    sender = relationship("User", back_populates="mail")

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    mail =  relationship("SentMailHistory", back_populates="sender")

class ListOfCompanies(Base):
    __tablename__ = 'list_of_companies'
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False, unique=True)
    company_email = Column(String, nullable=False, unique=True)
    added_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    last_time_mailed = Column(TIMESTAMP(timezone=True))
