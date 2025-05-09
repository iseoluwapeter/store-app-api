from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload
from database import engine, SessionLocal
from models import model
from models.model import Product, Supplier, Category
from pydantic import BaseModel, Field
from typing import List, Optional,Annotated
from utils.security import hash_password



product_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    desc: str
    unit: str
    price: float
    quantity: int
    status: int
    other_details: str| None = None
    supplier_id : int
    category_id: int

@product_router.post("/product", status_code=201)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == product.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=400, detail="Supplier not found")

    # Check if category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")

    # All good, create the product
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message": "Product created successfully",
        "product_id": new_product.id
    }



@product_router.get("/", status_code=200)
async def product(db: dbDep):
    products = db.query(Product).order_by(Product.name).all()

    return products

@product_router.get("/product/{product_id}", status_code=200)
async def product(db: dbDep, product_id: int = Path(..., gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
         raise HTTPException(status_code=404, detail="product not found!")

    return product

@product_router.put("/role/{product_id}", status_code=201)
async def product(db: dbDep, product_req: ProductCreate, product_id: int = Path(..., gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found, Check again!")
    product.name = product_req.name
    product.desc = product_req.desc
    product.unit = product_req.unit
    product.price = product_req.price
    product.quantity = product_req.quantity
    product.status = product_req.status
    product.other_details = product_req.other_details

    db.add(product)
    db.commit()
    return{" Product succesfully updated"}

@product_router.delete("/role/{product_id}" ,status_code=200)
async def product(db: dbDep, product_id: int = Path(..., gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(product)
    db.commit()
    return {"successful deleted a product"}