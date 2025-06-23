from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload
from database import engine, SessionLocal
from models import model
from models.model import Order, Customer
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


order_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class OrderCreate(BaseModel):
    customer_id: int
    date_of_order: datetime = datetime.utcnow()



@order_router.post("/order", status_code=200)
# async def order(db:dbDep, order:OrderCreate ):
#     customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
#     if customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found, Please check again")
#     new_order = Order(**order.dict())
#     db.add(new_order)
#     db.commit()
#     return {
#         "message": "Order successfully created!",
#         "order_id": new_order.id
#     }

async def create_order(order: OrderCreate, db: dbDep):
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_order = Order(
        customer_id=order.customer_id,
        date_of_order=order.date_of_order
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order created successfully",
        "order_id": new_order.id
    }

@order_router.get("/")
async def order(db:dbDep):
    order = db.query(Order).options(joinedload(Order.customer)).order_by(Order.id).all()
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found")
    return order

@order_router.get("/order/{order_id}")
async def order(db:dbDep, order_id: int = Path(..., gt=0)):
    order = db.query(Order).options(joinedload(Order.customer)).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    return{
        "Order Date": order.date_of_order,
        "Order Description": order.order_details,
        "Ordered_ by": order.customer.firstname
    }

@order_router.get("/orders-by-customers")
async def order_by_customer(db:dbDep):
    customers = db.query(Customer).options(joinedload(Customer.orders)).all()

    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    
    result = []
    for customer in customers:
        result.append({
            "customer_id": customer.id,
            "customer name": f"{customer.firstname} {customer.lastname}",
            "order_count": len(customer.orders)
        })

    return result




@order_router.put("/order/{order_id}", status_code=200)
async def order(db:dbDep, order_req: OrderCreate, order_id: int = Path(..., gt=0)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order Not Found, Please check again")
    
    order.order_details = order_req.order_details
    db.add(order)
    db.commit()
    return{
        "Order Completed"
    }

order_router.delete("/order/{order_id}", status_code=200)
async def order(db:dbDep, order_id: int = Path(..., gt=0)):
    order = db.query(Order).filter(Order.id == order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist, Please check again")
    db.delete(order)
    db.commit()
