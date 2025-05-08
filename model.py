
from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, func, ForeignKey
from database import Base
from sqlalchemy.orm import validates, relationship

class SentMailHistory(Base):
    __tablename__ = 'history'
    mail_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('list.id'))
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    sender = relationship("User", back_populates="mail")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    nickname = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    mail =  relationship("SentMailHistory", back_populates="sender")

class ListOfCompanies(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    added_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    last_time_mailed = Column(TIMESTAMP(timezone=True))
