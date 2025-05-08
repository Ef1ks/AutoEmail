import model
from database import engine
from fastapi import FastAPI

model.Base.metadata.create_all(bind=engine)

from router import wyslij, addToDB, user, auth, emailhistory

from funkcje.folder import create_dir
import os


app = FastAPI()

app.include_router(wyslij.router)

app.include_router(addToDB.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(emailhistory.router)
