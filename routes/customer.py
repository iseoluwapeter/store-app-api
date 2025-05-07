from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import model
from models.model import Customer as customerModel, Staff
from typing import Annotated, Literal
from pydantic import BaseModel, Field


customer_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class CustomerCreate(BaseModel):
    firstname: str = Field(..., min_length=3, max_length=30)
    lastname: str = Field(..., min_length=3, max_length=30)
    address: str 
    phone: int
    email: str = Field(..., min_length=8)
    staff_id: int




@customer_router.get("/")
async def get_all_customers(db:dbDep):
    customers = db.query(customerModel).order_by(customerModel.firstname).all()
    cust = []
    for customer in customers:
        cust.append({
            'Surname': customer.lastname,
            'Firstname': customer.firstname,
            'Middlename': customer.middle,
            'Password': customer.password,
            'Sex': customer.gender,
            'email': customer.email,
            'Phone': "0" + customer.phone

        })

    return cust

@customer_router.get("/customer/{customer_id}")
async def get_customer_by_Id(db:dbDep, customer_id: int = Path(..., gt=0)):
    customer = db.query(customerModel).filter(customerModel.id == customer_id).first()
    if not customer :
        raise HTTPException(status_code=404, detail="User does not exist")
    
    return customer

@customer_router.post("/customer", status_code=201)
async def customer(db:dbDep, customer:CustomerCreate):
    staff = db.query(Staff).filter(Staff.id == customer.staff_id).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff Not Found, Please Check again!")
    
    new_customer = customerModel(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh()
    return {
        "message": "Customer created successfully",
        "customer_id": new_customer.id,
        "registered_by": staff.firstname
    }

@customer_router.put("/customer/{customer_id}", status_code=204)
async def customer(db:dbDep, customer_req: CustomerCreate, customer_id:int = Path(..., gt=0) ):
    custom = db.query(customerModel).filter(customerModel.id == customer_id).first()
    if custom is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")
    custom.firstname = customer_req.firstname
    custom.lastname = customer_req.lastname
    custom.address= customer_req.address
    custom.email= customer_req.email
    custom.phone = customer_req.phone
    db.add(custom)
    db.commit()

@customer_router.delete("/customer/{customer_id}", status_code=204)
async def customer(db:dbDep, customer_id: int = Path(..., gt=0)):
    custom = db.query(customerModel).filter(customerModel.id == customer_id).first()

    if custom is None:
        raise HTTPException(status_code=404, detail="User Not Found, Check again!")
    deleted_customer = db.delete(custom)
    db.commit()
    return {deleted_customer}
