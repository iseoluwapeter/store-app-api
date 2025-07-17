from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session, joinedload
from database import engine, SessionLocal
from models import model
from models.model import Staff, Role
from pydantic import BaseModel, Field
from typing import List, Optional,Annotated
from utils.security import hash_password



staff_router = APIRouter()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]
lgDep = Annotated[Session, Depends()]

class StaffCreate(BaseModel):
    firstname: str = Field(..., min_length=2)
    lastname: str = Field(..., min_length=2)
    address: str
    phone: str
    email: str
    username: str
    password: str
    role_id: int 

@staff_router.get("/")
async def list_staff(db: dbDep):
    staff_list = db.query(Staff).order_by(Staff.id).all()
    return staff_list

@staff_router.get("/staff/{staff_id}")
async def staff(db:dbDep, staff_id:int = Path(..., gt=0)):
    staff = db.query(Staff).options(joinedload(Staff.role)).filter(Staff.id ==staff_id).first()

    if staff is None:
        raise HTTPException(status_code=404, detail="Staff does not exist. Please check again!")
    
    return {
        "Fullname": f"{staff.firstname} {staff.lastname}",
        "Address": staff.address,
        "Username": staff.username,
        "Phone Number": staff.phone,
        "email": staff.email,
        "Role": staff.role.name,

    }

@staff_router.post("/staff", status_code=201)
async def create_staff(staff: StaffCreate, db: dbDep):

    role = db.query(Role).filter(Role.id == staff.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

 
    existing = db.query(Staff).filter(Staff.username == staff.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    staff_credentials = staff.dict()
    staff_credentials["password"] = hash_password(staff_credentials["password"])

    new_staff = Staff(**staff_credentials)
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return {
        "message": "Staff created successfully",
        "staff_id": new_staff.id,
        "assigned_role": role.name
    }


@staff_router.put("/staff/{staff_id}")
async def staff(db: dbDep, staff_req: StaffCreate, staff_id: int = Path(..., gt=0)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()

    if staff is None:
        raise HTTPException(status_code=404, detail="Staff Not Found, Please check again")
    staff.firstname = staff_req.firstname
    staff.lastname = staff_req.lastname
    staff.email = staff_req.email
    staff.address = staff_req.address
    db.add(staff)
    db.commit() 

@staff_router.delete("/staff/{staff_id}")
async def staff(db: dbDep, staff_id: int =Path(..., gt=0)):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff Not Found, Please check again")
    db.delete(staff)
    db.commit()
  
    return{"Staff succesfully deleted"}
