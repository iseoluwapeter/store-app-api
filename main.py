from fastapi import FastAPI
from routes import customer, role, staff, category,  order
from database import Base, engine

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

app.include_router(role.role_router, prefix="/role", tags=["role"])
app.include_router(staff.staff_router, prefix="/staff", tags=["staff"])
app.include_router(customer.customer_router, prefix="/customer", tags=["customers"])
app.include_router(category.category_router, prefix="/category", tags=["category"])
app.include_router(order.order_router, prefix="/order", tags=["order"])
