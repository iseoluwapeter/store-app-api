from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import model
from models.model import Category
from pydantic import BaseModel, Field
from typing import Annotated


category_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    description: str | None = None

@category_router.get("/")
async def category(db: dbDep):
    category_list = db.query(Category).order_by(Category.name).all()
    if category is None:
        raise HTTPException(status_code=404, detail="Category Does not Exist")
    
    return category_list

@category_router.get("/category/{category_id}")
async def category(db: dbDep, category_id: int = Path(..., gt=0)):
    single_category = db.query(Category).filter(Category.id == category_id).first()

    if single_category is None:
        raise HTTPException(status_code=404, detail="categoty not found!")
    return single_category

@category_router.post("/category")
async def category(db:dbDep, category: CategoryCreate):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()

@category_router.put("/category/{category_id}")
async def category(db: dbDep, category_req: CategoryCreate, category_id: int = Path(..., gt=0)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Catgory not found, Check again!")
    category.name = category_req.name
    category.description = category_req.description
    db.add(category)
    db.commit()
    return{"category updated succesfully"}
