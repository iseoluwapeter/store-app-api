from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from models import model
from models.model import Staff
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv
from utils.security import verify_password

load_dotenv()

auth_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

bycrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth_bearer = OAuth2PasswordBearer("/auth/login")

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

def get_current_user(token: Annotated[str, Depends(oauth_bearer)], db: dbDep):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms="HS256")
        staff_id : int = payload.get("id")
        if staff_id is None:
            raise HTTPException(status_code=404, detail="Invalid token: No ID")
    except JWTError:
        raise HTTPException(status_code=404, detail="Invalid token")
    
    staff = db.query(Staff).filter(Staff.id == staff).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="staff not found")
    return staff


@auth_router.post("/login")
async def login_access(requestForm:Annotated[OAuth2PasswordRequestForm, Depends()], db:dbDep):
    username = requestForm.username
    pas = requestForm.password

    #get staff from db
    staff = db.query(Staff).filter(Staff.email == username).first()
    if not staff:
        raise HTTPException( status_code=404, detail="staff cannot be recognized",)
    
    if  not verify_password(pas, staff.password):
        raise HTTPException(status_code=401, detail= "Invalid credentials")
    
    token = create_token(staff.email, staff.id, timedelta(minutes=30))
    return {
        "access_token": token,
        "token_type": "bearer",
        "staff_id": staff.id,
        "email":staff.email
    }
 