from fastapi import FastAPI
from routes import customer, role, staff, category,  order, supplier, product, payment, orderdetails
from database import Base, engine

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)

app.include_router(role.role_router, prefix="/role", tags=["role"])
app.include_router(supplier.supplier_router, prefix="/supplier", tags=["supplier"])
app.include_router(staff.staff_router, prefix="/staff", tags=["staff"])
app.include_router(customer.customer_router, prefix="/customer", tags=["customers"])
app.include_router(category.category_router, prefix="/category", tags=["category"])
app.include_router(order.order_router, prefix="/order", tags=["order"])
app.include_router(product.product_router, prefix="/product", tags=["product"])
app.include_router(payment.payment_router, prefix="/payment", tags=["payment"])
app.include_router(orderdetails.orderdetails_router, prefix="/order_details", tags=["order_details"])



