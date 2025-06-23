# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Supplier, Role, Staff, Customer, Category, Product, Order, OrderDetail, Payment
from pydantic import BaseModel
from typing import Optional
import datetime

app = FastAPI()

# SQLite setup
DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class SupplierCreate(BaseModel):
    Name: str
    Address: str
    phone: int
    fax: int
    Email: str
    other_details: str

class SupplierEdit(SupplierCreate):
    pass

class OrderCreate(BaseModel):
    Date_of_Order: datetime.date
    Order_Details: str
    Customer_ID: int

class OrderEdit(OrderCreate):
    pass

@app.post("/supplier/")
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.put("/supplier/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierEdit, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.Supplier_ID == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.post("/order/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.put("/order/{order_id}")
def update_order(order_id: int, order: OrderEdit, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.Order_ID == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order