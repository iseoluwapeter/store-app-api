from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload
from database import engine, SessionLocal
from models import model
from models.model import OrderDetail, Payment, Order, Product
from pydantic import BaseModel, Field
from typing import List, Optional,Annotated
from utils.security import hash_password
from datetime import datetime



orderdetails_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class OrderDetailCreate(BaseModel):
    unit_price: float = Field(..., ge=0.01)
    size: int
    quantity: int
    discount:int
    total:float 
    date:datetime
    product_id: int
    order_id : int
    bill_number: int

@orderdetails_router.post("/orderdetails", status_code=201)
async def order_details(order_details: OrderDetailCreate, db: Session = Depends(get_db)):

    # Check if payment reference exists
    
    bill_number = db.query(Payment).filter(Payment.bill_number == order_details.bill_number).first()
    if not bill_number:
        raise HTTPException(status_code=400, detail="Payment record cannot be found")

    # Check if product exists
    product = db.query(Product).filter(Product.id == order_details.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product is unavailable")
    
     # Check if order record exists
    order = db.query(Order).filter(Order.id == order_details.order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="You are yet to place an order")

    new_order_details = OrderDetail(**order_details.dict())
    db.add(new_order_details)
    db.commit()
    db.refresh(new_order_details)
    return {
        "message": "Order record created",
        "new order details": new_order_details.id
    }



@orderdetails_router.get("/", status_code=200)
async def order_details(db: dbDep):
    order_detail = db.query(OrderDetail).order_by(OrderDetail.id).all()

    return order_detail

@orderdetails_router.get("/orderdetails/{orderdetails_id}", status_code=200)
async def orderdetails(db: dbDep, orderdetails_id: int = Path(..., gt=0)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == orderdetails_id).first()

    if order_detail is None:
         raise HTTPException(status_code=404, detail="cannot find order details")

    return order_detail
