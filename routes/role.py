from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import model
from models.model import Role
from typing import Annotated
from pydantic import BaseModel, Field


role_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]

class RoleCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    desc: str 

@role_router.post("/role", status_code=201)
async def role(db:dbDep, role: RoleCreate):
    new_role = Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return("role successfully added")

@role_router.get("/", status_code=200)
async def role(db: dbDep):
    roles = db.query(Role).order_by(Role.name).all()

    return [{"role": role.name,"description": role.desc } for role in roles]

@role_router.put("/role/{role_id}", status_code=201)
async def role(db: dbDep, role_req: RoleCreate, role_id: int = Path(..., gt=0)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found, Check again!")
    role.name = role_req.name
    role.desc = role_req.desc
    db.add(role)
    db.commit()
    return{" Role succesfully updated"}

@role_router.delete("/role/{role_id}" ,status_code=200)
async def role(db: dbDep, role_id: int = Path(..., gt=0)):
    role = db.query(Role).filter(Role.id == role_id).first()
    db.delete(role)
    db.commit()
    return {"successful deleted a role"}
 

