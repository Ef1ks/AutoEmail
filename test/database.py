from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





