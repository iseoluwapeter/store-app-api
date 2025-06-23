from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from models.model import Customer, Staff
from typing import Annotated
from pydantic import BaseModel, Field
from database import SessionLocal
# from .auth import get_current_user

customer_router = APIRouter()

# Helper function to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]
# cust-depend = Annotated[dict, Depends(get_current_user)]

# Pydantic model for customer creation input
class CustomerCreate(BaseModel):
    firstname: str = Field(..., min_length=3, max_length=30)
    lastname: str = Field(..., min_length=3, max_length=30)
    address: str
    phone: str
    email: str = Field(..., min_length=8)
    staff_id: int

@customer_router.post("/customer", status_code=201)
async def create_customer(db: dbDep, customer: CustomerCreate):
    # Check if the staff exists
    staff = db.query(Staff).filter(Staff.id == customer.staff_id).first()
    
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with ID {customer.staff_id} not found."
        )

    # Create a new customer if staff exists
    new_customer = Customer(**customer.dict())  
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer successfully created!",
        "customer_id": new_customer.id
    }


@customer_router.get("/")
async def get_all_customers(db:dbDep):
    customers = db.query(Customer).order_by(Customer.id).all()
    

    return customers

@customer_router.get("/customer/{customer_id}")
async def get_customer_by_Id(db:dbDep, customer_id: int = Path(..., gt=0)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer :
        raise HTTPException(status_code=404, detail="User does not exist")
    
    return customer






@customer_router.put("/customer/{customer_id}", status_code=204)
async def customer(db:dbDep, customer_req: CustomerCreate, customer_id:int = Path(..., gt=0) ):
    custom = db.query(Customer).filter(Customer.id == customer_id).first()
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
    custom = db.query(Customer).filter(Customer.id == customer_id).first()

    if custom is None:
        raise HTTPException(status_code=404, detail="User Not Found, Check again!")
    deleted_customer = db.delete(custom)
    db.commit()
    return {"customer deleted"}
