from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload
from database import engine, SessionLocal
from models import model
from models.model import Supplier
from pydantic import BaseModel, Field
from typing import List, Optional,Annotated
from utils.security import hash_password



supplier_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class SupplierCreate(BaseModel):
    name: str = Field(..., min_length=2)
    address: str
    phone: str
    email: str
    other_details: str| None = None


@supplier_router.post("/supplier", status_code=200)
async def supplier(db:dbDep, supplier: SupplierCreate ):
    new_suppler = Supplier(**supplier.dict())
    db.add(new_suppler)
    db.commit()

    return{"Created succesfully"}

@supplier_router.get("/", status_code=200)
async def supplier(db: dbDep):
    suppliers = db.query(Supplier).order_by(Supplier.id).all()

    return suppliers

@supplier_router.get("/supplier/{supplier_id}")
async def supplier( db:dbDep, supplier_id: int = Path(..., gt=0)):
    single_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not single_supplier:
        raise HTTPException(status_code=404, detail="Supplier Not Found")
    return single_supplier

# @product_router.get("/product/{product_id}", status_code=200)
# async def product(db: dbDep, product_id: int = Path(..., gt=0)):
#     product = db.query(Product).filter(Product.id == product_id).first()

#     if product is None:
#          raise HTTPException(status_code=404, detail="product not found!")

#     return product

@supplier_router.put("/supplier/{supplier_id}", status_code=201)
async def supplier(db: dbDep, supplier_req: SupplierCreate, supplier_id: int = Path(..., gt=0)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="supplier not found, Check again!")
    supplier.name = supplier_req.name
    supplier.address = supplier_req.address
    supplier.phone = supplier_req.phone
    supplier.email = supplier_req.email

    db.add(supplier)
    db.commit()
    return{" Supplier succesfully updated"}

@supplier_router.delete("/supplier/{supplier_id}" ,status_code=200)
async def supplier(db: dbDep, supplier_id: int = Path(..., gt=0)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier does not exist please check again")
    db.delete(supplier)
    db.commit()
    return {"successful deleted a supplier"}