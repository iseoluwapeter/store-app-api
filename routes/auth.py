from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from models import model
from models.model import Staff
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv

load_dotenv()

auth_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

bycrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRET_KEY = os.getenv("SECRET_KEY")
def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close() 
dbDep = Annotated[Session,Depends(get_db)]


def create_token(email:str, staff_id:int, expires:timedelta):
    #process the expire time
    exp = datetime.now()+expires
    ex = {'sub':email, 'id':staff_id, 'exp': exp}
    return jwt.encode(ex, SECRET_KEY, 'HS256')

# def get_current_user():

@auth_router.post("/login")
async def login_access(requestForm:Annotated[OAuth2PasswordRequestForm, Depends()], db:dbDep):
    username = requestForm.username
    pas = requestForm.password

    #get staff from db
    staff = db.query(Staff).filter(Staff.email == username).first()
    if not staff:
        raise HTTPException( status_code=404, detail="staff cannot be recognized",)
    
    if not bycrypt_context.verify(pas, staff.password):
        return "Username/Password doesnot match"
    token = create_token(staff.email, staff.id, timedelta(minutes=30))
    return {
        "access_token": token,
        "token_type": "bearer",
        "staff_id": staff.id,
        "email":staff.email
    }
 