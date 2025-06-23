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
    order_id: int
    product_id: int
    bill_number: int | None = None
    unit_price: float
    quantity: int
    discount: float = 0




@orderdetails_router.post("/order/order")
async def create_order_detail(detail: OrderDetailCreate, db: dbDep):
    product = db.query(Product).filter(Product.id == detail.product_id).first()
    order = db.query(Order).filter(Order.id == detail.order_id).first()

    if not product or not order:
        raise HTTPException(status_code=404, detail="Order or Product not found")

    total_price = (detail.unit_price * detail.quantity) - detail.discount

    new_detail = OrderDetail(
        product_id=detail.product_id,
        order_id=detail.order_id,
        unit_price=detail.unit_price,
        quantity=detail.quantity,
        discount=detail.discount,
        total=total_price,
        date=datetime.utcnow()
    )
    db.add(new_detail)
    db.commit()
    db.refresh(new_detail)

    return {
        "message": "Order detail added successfully",
        "order_detail_id": new_detail.id
    }


@orderdetails_router.get("/", status_code=200)
async def order_details(db: dbDep):
    order_detail = db.query(OrderDetail).order_by(OrderDetail.id).all()

    results = []

    for order in order_detail:
        results.append({
            "id": order.id,
            "customer": order.order.customer,
            "order_date": order.date,
            "product": order.product.name,
            "unit_price": order.unit_price,
            "quantity":order.quantity,
            "total":order.total,
            "payment": order.payment

        })
    return results
       

@orderdetails_router.get("/orderdetails/{orderdetails_id}", status_code=200)
async def orderdetails(db: dbDep, orderdetails_id: int = Path(..., gt=0)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == orderdetails_id).first()

    if order_detail is None:
         raise HTTPException(status_code=404, detail="cannot find order details")

    return order_detail
