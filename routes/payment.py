from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import model
from models.model import Payment
from typing import Annotated
from pydantic import BaseModel, Field


payment_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class PaymentCreate(BaseModel):
    payment_type: str = Field(..., min_length=3, max_length=50)
    other_details: str 

@payment_router.post("/payment", status_code=201)
async def payment(db:dbDep, payment: PaymentCreate):
    new_payment = Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return("payment successfull")

@payment_router.get("/", status_code=200)
async def payment(db: dbDep):
    payment = db.query(Payment).order_by(Payment.bill_number).all()

    if payment is None:
        raise HTTPException(status_code=404, detail="Payment cannot be found")

    return  payment

@payment_router.get("/payment/{bill_number}", status_code=200)
async def payment(db: dbDep, bill_number: int = Path(..., gt=0)):
    payment = db.query(Payment).order_by(Payment.bill_number == bill_number).first()

    if payment is None:
        raise HTTPException(status_code=404, detail="Payment cannot be found")

    return  payment


 

